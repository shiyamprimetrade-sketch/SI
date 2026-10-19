/* Numeric conformance probe: exact integer decimal inputs, binary64 bits, repr.
   This deliberately has a narrow JSON protocol and no Python dependency. */
'use strict';
const fs=require('node:fs');
const {rationalDivide,pythonFloatString,compareNumeric}=require('./vm.js');
function bitsOf(v) {
  const buf=new ArrayBuffer(8),dv=new DataView(buf);
  dv.setFloat64(0,v,false);
  return dv.getBigUint64(0,false).toString(16).padStart(16,'0');
}
function fromBits(hex) {
  if(!/^[0-9a-fA-F]{16}$/.test(hex))throw Error('invalid binary64 bit vector');
  const buf=new ArrayBuffer(8),dv=new DataView(buf);
  dv.setBigUint64(0,BigInt('0x'+hex),false);
  return dv.getFloat64(0,false);
}
function execute(item){
 try{
  if(item.kind==='ratio'){
   const v=rationalDivide(BigInt(item.a),BigInt(item.b));
   return {ok:true,bits:bitsOf(v),text:pythonFloatString(v)};
  }
  if(item.kind==='bits'){
   const n=fromBits(item.hex);
   if(!Number.isFinite(n))return {ok:false,error:'non-finite numeric result'};
   return {ok:true,bits:bitsOf(n),text:pythonFloatString(n)};
  }
  if(item.kind==='compare'){
   const x={kind:'int',value:BigInt(item.integer)};
   const y={kind:'float',value:fromBits(item.hex)};
   return {ok:true,comparison:compareNumeric(x,y)};
  }
  throw Error('unknown probe kind');
 }catch(e){return {ok:false,error:String(e.message)};}
}
function main(){
 const xs=JSON.parse(fs.readFileSync(0,'utf8'));
 if(!Array.isArray(xs)||xs.length>2000)throw Error('invalid batch');
 process.stdout.write(JSON.stringify(xs.map(execute))+'\n');
}
if(require.main===module)main();
module.exports={execute};
