// Browser integration against the running loopback app. No external retrieval.
// Run: node tests/ui_smoke.mjs
import {spawn} from 'node:child_process';
import {mkdtempSync, mkdirSync, writeFileSync, rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import baseAssert from 'node:assert/strict';
let assertionCount=0;const assert=new Proxy(baseAssert,{get(target,key){const value=target[key];return typeof value==='function'?(...args)=>{assertionCount++;return value(...args);}:value;}});
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
let session;const createdIds=[];
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
 await evaluate("document.getElementById('letterOperation').value='reverse-letters-v1';document.getElementById('transformLetters').click()");
 await until("document.getElementById('letterResult').textContent.includes('םולש')");
 assert.match(await evaluate("document.getElementById('letterResult').textContent"),/input_start/);
 await evaluate("document.getElementById('transformGrid').click()");
 await until("document.getElementById('gridResult').textContent.includes('input_coordinates')");
 assert.match(await evaluate("document.getElementById('gridResult').textContent"),/RECONSTRUCTION/);
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
 await evaluate("document.querySelector('[data-view=psalms]').click();document.getElementById('verseEdition').value='Synthetic coordinate edition';document.getElementById('verseStart').value='2';document.getElementById('verseEnd').value='3';document.getElementById('makeVerseReference').click()");
 await until("document.getElementById('verseReference').textContent.includes('UNVERIFIED')");
 assert.match(await evaluate("document.getElementById('verseReference').textContent"),/Synthetic coordinate edition/);
 // Private notebook UI: only project-original synthetic content; remove after test.
 await evaluate("document.querySelector('[data-view=notebook]').click()");
 await until("document.querySelectorAll('#coordinateSource option').length===27");
 await evaluate("newDocument('journal');document.getElementById('documentTitle').value='Synthetic browser journal';document.getElementById('documentText').value='Original browser exercise';document.getElementById('saveDocument').click()");
 await until("document.getElementById('notebookStatus').textContent.includes('revision 1')");
 const journalId=await evaluate('notebookItem.id');createdIds.push(journalId);
 await evaluate("document.getElementById('documentText').value='Revised original exercise';document.getElementById('saveDocument').click()");
 await until("document.getElementById('revisionHistory').options.length===2");
 await evaluate("document.getElementById('revisionHistory').value='1';document.getElementById('restoreRevision').click()");
 assert.equal(await evaluate("document.getElementById('documentText').value"),'Original browser exercise');
 await evaluate("newDocument();document.getElementById('documentTitle').value='Synthetic transcription';document.getElementById('coordinateSource').value='sloane-3188';document.getElementById('coordinateEdition').value='Original exercise, not manuscript text';document.getElementById('coordinatePage').value='Synthetic page';document.getElementById('documentAttribution').value='Browser fixture';document.getElementById('transcriptionRights').value='Project original';document.getElementById('textDirection').value='rtl';document.getElementById('textDirection').dispatchEvent(new Event('change'));document.getElementById('documentText').value='שלום <img src=x onerror=alert(1)>';document.getElementById('saveDocument').click()");
 await until("notebookItem?.document.kind==='transcription'");
 const transcriptionId=await evaluate('notebookItem.id');createdIds.push(transcriptionId);
 assert.equal(await evaluate("getComputedStyle(document.getElementById('documentText')).direction"),'rtl');
 assert.equal(await evaluate("document.querySelectorAll('#revisionPreview img').length"),0,'Imported text remains inert');
 assert.equal(await evaluate("document.getElementById('exportTEI').disabled"),false);
 assert.match(await evaluate("document.getElementById('revisionPreview').textContent"),/sloane-3188/);
 await evaluate("newDocument('relationship');document.getElementById('documentTitle').value='Synthetic comparison';document.getElementById('coordinateSource').value='sloane-3188';document.getElementById('coordinateEdition').value='Synthetic exercise';document.getElementById('coordinatePage').value='Synthetic page';document.getElementById('documentAttribution').value='Browser fixture';document.getElementById('relationshipSubject').value='sloane-3188';document.getElementById('relationshipObject').value='sloane-3189';document.getElementById('relationshipPredicate').value='resembles';document.getElementById('documentText').value='Synthetic hypothesis only; no historical assertion';document.getElementById('saveDocument').click()");
 await until("notebookItem?.document.kind==='relationship'");
 const relationId=await evaluate('notebookItem.id');createdIds.push(relationId);
 await evaluate("document.querySelector('[data-view=graph]').click()");
 await until("document.getElementById('graphEdges').textContent.includes('Synthetic hypothesis only')");
 assert.match(await evaluate("document.getElementById('graphEdges').textContent"),/HYPOTHESIS/);
 assert.equal(await evaluate("document.querySelectorAll('#graphEdges details').length"),1);
 assert.equal(await evaluate('document.documentElement.scrollWidth<=window.innerWidth'),true,'Graph mobile overflow');
 await evaluate("document.querySelector('[data-view=lab]').click();document.getElementById('saveManifest').click()");
 await until("manifestRecord!==null");
 const manifestId=await evaluate('manifestRecord.id');createdIds.push(manifestId);
 const savedHash=await evaluate('location.hash');
 assert.match(savedHash,/^#manuscript\//);
 await send('Page.reload',{},session);
 await until("manuscript?.pages.length===2 && manifestRecord!==null");
 assert.equal(await evaluate('location.hash'),savedHash);
 assert.equal(await evaluate("document.getElementById('manifestImage').hasAttribute('src')"),false);
 assert.equal(await evaluate("document.getElementById('showPage').disabled"),true,'Local-only image request disabled');
 await evaluate("document.getElementById('transcribePage').click()");
 await until("document.getElementById('coordinateCanvas').value.includes('canvas/')");
 assert.equal(await evaluate("document.getElementById('documentText').value"),'','No inferred transcription');
 await evaluate("document.querySelector('[data-view=notebook]').focus()");
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight'},session);
 assert.equal(await evaluate('document.activeElement.dataset.view'),'graph','Keyboard section navigation');
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,nativeVirtualKeyCode:13,text:'\r',unmodifiedText:'\r'},session);
 await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,nativeVirtualKeyCode:13},session);
 await until("!document.getElementById('graph').classList.contains('hidden')");
 for(const id of [journalId,transcriptionId,relationId,manifestId])await evaluate(`(async()=>{const r=await api('/api/notebook/${id}');await api('/api/notebook/${id}?expected_revision='+r.revision,'DELETE');})()`);
 assert.deepEqual(await evaluate("api('/api/notebook')"),[],'Synthetic browser records cleaned');
 // Visible focus and semantic label smoke; screen reader audit remains manual.
 await evaluate("document.querySelector('[data-view=sources]').click();document.getElementById('sourceQuery').focus()");
 assert.equal(await evaluate("document.activeElement.id"),'sourceQuery');
 assert.equal(await evaluate("document.querySelectorAll('label[for=sourceQuery]').length"),1);
 assert.deepEqual(errors,[]);
 assert.deepEqual(externalRequests,[],'Unexpected external request');
 const missingLabels=await evaluate("[...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(e=>!e.labels?.length&&!e.getAttribute('aria-label')&&!e.getAttribute('aria-labelledby')).map(e=>e.id)");
 assert.deepEqual(missingLabels,[],'All form controls have an accessible name source');
 const paletteContrast=await evaluate(`(()=>{const rgb=h=>h.match(/../g).map(x=>parseInt(x,16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);const lum=h=>{const [r,g,b]=rgb(h);return .2126*r+.7152*g+.0722*b;};const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};return {mutedOnSurface:ratio('aeb9c9','13182a'),textOnInput:ratio('f6f0e7','0c1222'),focusOnSurface:ratio('5de2f0','13182a')};})()`);
 for(const ratio of Object.values(paletteContrast))assert.ok(ratio>=4.5,'Sampled palette contrast');
 const evidence={browser:(await send('Browser.getVersion')).product,assertions:assertionCount,consoleExceptions:errors,externalRequests,
   viewports:['1440x1100','390x844'],remoteImagesRequested:false,paletteContrast,formControlsWithoutName:missingLabels,
   limitations:'No full WCAG audit, screen reader, real institution or human-use verification'};
 writeFileSync('docs/execution/evidence/ui-smoke.json',JSON.stringify(evidence,null,2)+'\n');
 console.log(JSON.stringify(evidence));
}finally{for(const id of createdIds){await evaluate(`(async()=>{const r=await fetch('/api/notebook/${id}');if(r.ok){const item=await r.json();await fetch('/api/notebook/${id}?expected_revision='+item.revision,{method:'DELETE'});}})()`).catch(()=>{});}clearTimeout(timeout);await send('Browser.close').catch(()=>{});browser.kill();rmSync(profile,{recursive:true,force:true});}
