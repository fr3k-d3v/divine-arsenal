// Browser integration against the running loopback app. No external retrieval.
// Run: node tests/ui_smoke.mjs
import {spawn} from 'node:child_process';
import {mkdtempSync, mkdirSync, writeFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import assert from 'node:assert/strict';
const profile=mkdtempSync(join(tmpdir(),'divine-browser-'));
const browser=spawn('chromium',['--headless','--no-sandbox','--disable-gpu','--disable-background-networking',
 '--no-first-run','--no-default-browser-check','--disable-component-update',
 '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1',
 '--remote-debugging-pipe','--user-data-dir='+profile],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let next=0,buffer='';const pending=new Map(),errors=[],externalRequests=[];
browser.stdio[4].on('data',data=>{buffer+=data.toString();let end;while((end=buffer.indexOf('\0'))>=0){
 const item=JSON.parse(buffer.slice(0,end));buffer=buffer.slice(end+1);
 if(item.id){const p=pending.get(item.id);if(p){pending.delete(item.id);item.error?p.reject(Error(JSON.stringify(item.error))):p.resolve(item.result);}}
 if(item.method==='Network.requestWillBeSent' && !item.params.request.url.startsWith('http://127.0.0.1:8768/') && !item.params.request.url.startsWith('data:'))externalRequests.push(item.params.request.url);
 if(item.method==='Runtime.exceptionThrown')errors.push(item.params.exceptionDetails.text);
}});
function send(method,params={},sessionId){return new Promise((resolve,reject)=>{const id=++next;pending.set(id,{resolve,reject});browser.stdio[3].write(JSON.stringify({id,method,params,...(sessionId?{sessionId}:{})})+'\0');});}
const timeout=setTimeout(()=>{browser.kill();console.error('Browser check timed out');process.exit(1);},45000);
let session;
async function evaluate(expression){const result=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true},session);if(result.exceptionDetails)throw Error(JSON.stringify(result.exceptionDetails));return result.result.value;}
async function until(expression){for(let i=0;i<100;i++){if(await evaluate(expression))return;await new Promise(r=>setTimeout(r,50));}throw Error('Timed out: '+expression);}
try{
 const {targetId}=await send('Target.createTarget',{url:'about:blank'});
 session=(await send('Target.attachToTarget',{targetId,flatten:true})).sessionId;
 await send('Page.enable',{},session);await send('Runtime.enable',{},session);await send('Network.enable',{},session);
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false},session);
 await send('Page.navigate',{url:'http://127.0.0.1:8768/'},session);
 await until("document.getElementById('status')?.textContent.includes('LOCAL ENGINE')");
 await evaluate("document.querySelector('[data-view=sources]').click()");
 await until("document.querySelectorAll('.source-card').length===27 && document.querySelectorAll('.psalm-link').length===150");
 assert.equal(await evaluate("document.querySelectorAll('.psalter-book').length"),5);
 const links=await evaluate("[...document.querySelectorAll('.psalm-link')].map(a=>a.getAttribute('href'))");
 assert.equal(new Set(links).size,150);
 await evaluate("document.querySelector('[data-view=psalms]').click()");
 await evaluate("document.querySelectorAll('.psalm-link')[115].click()");
 await until("document.getElementById('selectedPsalm').textContent==='MT Psalm 116'");
 assert.match(await evaluate("document.getElementById('selectedPsalmBook').textContent"),/114\/115/);
 await evaluate("document.getElementById('psalmEdition').value='lxx-index';document.getElementById('psalmEdition').dispatchEvent(new Event('change'))");
 await until("document.getElementById('selectedPsalm').textContent==='LXX Psalm 1'");
 await evaluate("document.querySelectorAll('.psalm-link')[8].click()");
 await until("document.getElementById('selectedPsalm').textContent==='LXX Psalm 9'");
 assert.match(await evaluate("document.getElementById('selectedPsalmBook').textContent"),/psalm-009.*psalm-010/);
 await evaluate("document.querySelector('[data-view=sources]').click()");
 await evaluate("document.getElementById('sourceQuery').value='Liber Mysteriorum';document.getElementById('sourceQuery').dispatchEvent(new Event('input'))");
 await until("document.querySelectorAll('.source-card').length===1");
 assert.match(await evaluate("document.querySelector('.source-card').textContent"),/HYPOTHESIS/);
 await evaluate("document.querySelector('.source-card button').click()");
 assert.match(await evaluate("document.getElementById('sourceDetail').textContent"),/images rights: UNKNOWN/);
 mkdirSync('docs/execution/evidence',{recursive:true});
 await evaluate("document.getElementById('sourceQuery').value='';document.getElementById('sourceQuery').dispatchEvent(new Event('input'));document.getElementById('sourceDetail').classList.add('hidden')");
 await until("document.querySelectorAll('.source-card').length===27");
 writeFileSync('docs/execution/evidence/atlas-desktop.png',Buffer.from((await send('Page.captureScreenshot',{},session)).data,'base64'));
 await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true},session);
 assert.equal(await evaluate('document.documentElement.scrollWidth<=window.innerWidth'),true,'Source page overflow');
 writeFileSync('docs/execution/evidence/atlas-mobile.png',Buffer.from((await send('Page.captureScreenshot',{},session)).data,'base64'));
 await evaluate("document.querySelector('[data-view=lab]').click();document.getElementById('calculateHebrew').click()");
 await until("document.getElementById('languageResult').textContent.includes('376')");
 assert.equal(await evaluate("getComputedStyle(document.getElementById('hebrewInput')).direction"),'rtl');
 assert.equal(await evaluate("document.getElementById('hebrewInput').value"),'שלום');
 assert.equal(await evaluate("document.querySelectorAll('#traceRows tr').length"),4);
 const fixture=await import('node:fs').then(fs=>fs.readFileSync('tests/fixtures/iiif-synthetic.json','utf8'));
 await evaluate(`document.getElementById('manifestInput').value=${JSON.stringify(fixture)};document.getElementById('validateManifest').click()`);
 await until("document.querySelectorAll('#manifestPage option').length===2");
 assert.equal(await evaluate("document.getElementById('manifestImage').hasAttribute('src')"),false,'No silent remote images');
 await evaluate("document.getElementById('manifestPage').value='1';document.getElementById('manifestPage').dispatchEvent(new Event('change'))");
 assert.match(await evaluate("document.getElementById('pageCitation').textContent"),/canvas\/2/);
 assert.equal(await evaluate('document.documentElement.scrollWidth<=window.innerWidth'),true,'Lab page overflow');
 writeFileSync('docs/execution/evidence/lab-mobile.png',Buffer.from((await send('Page.captureScreenshot',{},session)).data,'base64'));
 await evaluate("document.querySelector('[data-view=studio]').click()");
 await until("document.querySelectorAll('#magicSquare span').length===9");
 assert.match(await evaluate("document.getElementById('magicMeta').textContent"),/constant 15/);
 // Test deep-link re-entry with explicit coordinate edition.
 await send('Page.navigate',{url:'http://127.0.0.1:8768/#psalm/lxx-index/113'},session);
 await until("document.getElementById('selectedPsalm')?.textContent==='LXX Psalm 113'");
 assert.match(await evaluate("document.getElementById('selectedPsalmBook').textContent"),/psalm-114.*psalm-115/);
 // Visible focus and semantic label smoke; screen reader audit remains manual.
 await evaluate("document.querySelector('[data-view=sources]').click();document.getElementById('sourceQuery').focus()");
 assert.equal(await evaluate("document.activeElement.id"),'sourceQuery');
 assert.equal(await evaluate("document.querySelectorAll('label[for=sourceQuery]').length"),1);
 assert.deepEqual(errors,[]);
 assert.deepEqual(externalRequests,[],'Unexpected external request');
 const evidence={browser:(await send('Browser.getVersion')).product,assertions:19,consoleExceptions:errors,externalRequests,
   viewports:['1440x1100','390x844'],remoteImagesRequested:false,
   limitations:'No full WCAG audit, screen reader, real institution or human-use verification'};
 writeFileSync('docs/execution/evidence/ui-smoke.json',JSON.stringify(evidence,null,2)+'\n');
 console.log(JSON.stringify(evidence));
}finally{clearTimeout(timeout);await send('Browser.close').catch(()=>{});browser.kill();rmSync(profile,{recursive:true,force:true});}
