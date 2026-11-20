const test=require('node:test'), assert=require('node:assert/strict');
require('../extension/src/shared.js');
const {classify,normalizeSettings,defaults}=global.NoShorts;
test('Shorts routes and channel routes',()=>{
 for(const u of ['/shorts/xyz','/shorts','/feed/shorts?x=1','https://m.youtube.com/shorts/xyz']) assert.equal(classify(u).kind,'shorts');
 for(const p of ['/@creator','/channel/UC123','/c/creator','/user/creator']) assert.equal(classify(p+'/shorts?x=1').target,'https://www.youtube.com'+p+'/videos');
});
test('Keep regular and external routes',()=>{for(const p of ['/watch?v=abc','/@myshorts/videos','/shortstuff/a','https://evil.example/shorts/a','/results?search_query=shorts','/playlist?list=shorts']) assert.equal(classify(p),null);});
test('Settings normalization',()=>{assert.deepEqual(normalizeSettings({enabled:false,blockDirect:'false',junk:1}),{...defaults,enabled:false});});
