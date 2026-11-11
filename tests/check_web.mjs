// Dependency-free syntax and document-identity checks; not a full HTML/a11y validator.
import {readFileSync} from 'node:fs';
import {Script} from 'node:vm';
import assert from 'node:assert/strict';
const html=readFileSync('divine/web/index.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length,1);
new Script(scripts[0][1],{filename:'divine/web/index.html'});
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
assert.equal(ids.length,new Set(ids).size,'Duplicate HTML IDs');
console.log(`JavaScript syntax valid; ${ids.length} unique HTML IDs`);
