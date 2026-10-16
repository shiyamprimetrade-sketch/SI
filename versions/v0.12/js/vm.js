// Independent SI-Portable-1 VM in JavaScript; numeric semantics approximated
// with BigInt + IEEE-754 Number, no Python execution imports.
'use strict';
const fs=require('node:fs');
const {parsePortable}=require('./portable.js');
const MAX_BITS=4096, MAX_OUTPUT=100000;
const err=msg=>{throw new Error(msg);};
const int=v=>({kind:'int',value:BigInt(v)});
const flt=v=>({kind:'float',value:v});
const check=x=>{
 if(x.kind==='int') {
   let z=x.value<0n?-x.value:x.value;
   if(z.toString(2).length>MAX_BITS)err('integer bit budget exceeded');
 }else if(x.kind==='float') {
   if(!Number.isFinite(x.value))err('non-finite numeric result');
 }else err('invalid numeric operand');
 return x;
};
function pythonFloatString(n){
 if(Object.is(n,-0))return '-0.0';
 let s=String(n);
 if(!s.includes('.')&&!s.includes('e'))s+='.0';
 // Python uses three exponent digits for magnitudes >=1e100, Javascript does not.
 if(s.includes('e')) {
   const [base,exp]=s.split('e');
   const signed=Number(exp);
   s=base+'e'+(signed>=0?'+':'-')+String(Math.abs(signed)).padStart(2,'0');
 }
 return s;
}
function fmt(x){check(x);return x.kind==='int'?x.value.toString():pythonFloatString(x.value);}
function toFloat(x){
 if(x.kind==='float')return x.value;
 const n=Number(x.value);
 if(!Number.isFinite(n))err('numeric overflow');
 return n;
}
function nonZero(x){return x.kind==='int'?x.value!==0n:x.value!==0;}
function binary(op,a,b){
 check(a);check(b);
 const ints=a.kind==='int'&&b.kind==='int';
 if(op==='EQ'||op==='LT'){
   if(ints)return int(op==='EQ'?(a.value===b.value?1:0):(a.value<b.value?1:0));
   const x=toFloat(a),y=toFloat(b);
   return int(op==='EQ'?(x===y?1:0):(x<y?1:0));
 }
 if(op==='DIV'){
   if(!nonZero(b))err('division by zero');
   const x=toFloat(a),y=toFloat(b);
   return check(flt(x/y));
 }
 if(ints){
   if(op==='ADD')return check(int(a.value+b.value));
   if(op==='SUB')return check(int(a.value-b.value));
   if(op==='MUL')return check(int(a.value*b.value));
 }
 const x=toFloat(a),y=toFloat(b);
 if(op==='ADD')return check(flt(x+y));
 if(op==='SUB')return check(flt(x-y));
 if(op==='MUL')return check(flt(x*y));
 err('invalid opcode');
}
function budget(v,label,defaultValue){
 if(v===undefined)v=defaultValue;
 if(!Number.isSafeInteger(v)||v<0)err('invalid '+label+' budget');
 return v;
}
function runPortable(source,options={}){
 const maxSteps=budget(options.max_steps,'step',10000);
 const maxStack=budget(options.max_stack,'stack',1024);
 const maxOutput=budget(options.max_output_chars,'output',MAX_OUTPUT);
 const code=parsePortable(source);
 let stack=[],output=[],steps=0,chars=0,pc=0;
 while(pc<code.length){
   if(steps>=maxSteps)err('step budget exceeded');
   const i=code[pc++],op=i.opcode;steps++;
   if(op==='PUSH')stack.push(check(int(i.operand)));
   else if(['ADD','SUB','MUL','DIV','LT','EQ'].includes(op)){
     if(stack.length<2)err('stack underflow');
     const b=stack.pop(),a=stack.pop();
     stack.push(binary(op,a,b));
   }else if(op==='DUP'){
     if(!stack.length)err('stack underflow');
     stack.push(stack[stack.length-1]);
   }else if(op==='SWAP'){
     if(stack.length<2)err('stack underflow');
     const a=stack.length-1;[stack[a],stack[a-1]]=[stack[a-1],stack[a]];
   }else if(op==='DROP'){
     if(!stack.length)err('stack underflow');stack.pop();
   }else if(op==='PRINT'){
     if(!stack.length)err('stack underflow');
     const v=fmt(stack.pop());
     if(chars+v.length>maxOutput)err('output budget exceeded');
     output.push(v);chars+=v.length;
   }else if(op==='JMP')pc=i.target;
   else if(op==='JZ'){
     if(!stack.length)err('stack underflow');
     if(!nonZero(stack.pop()))pc=i.target;
   }else if(op==='HALT')break;
   else if(op!=='LABEL')err('invalid opcode');
   if(stack.length>maxStack)err('stack budget exceeded');
 }
 return {output,stack:stack.map(x=>({kind:x.kind,text:fmt(x)})),steps};
}
function category(s){
 if(s.includes('budget exceeded')) return s;
 if(s.includes('underflow'))return 'stack underflow';
 if(s.includes('division by zero'))return 'division by zero';
 if(s.includes('numeric overflow'))return 'numeric overflow';
 if(s.includes('non-finite'))return 'non-finite numeric result';
 if(s.startsWith('invalid ')||s.includes('nonportable')||s.includes('bare CR')||s.includes('character at offset')||s.includes('unknown ')||s.includes('duplicate ')||s.includes('needs '))return 'parse error';
 return 'other error';
}
function evaluate(input){
 try {const x=runPortable(input.source,input.options||{});return {ok:true,...x};}
 catch(e){return {ok:false,category:category(String(e.message)),error:String(e.message)};}
}
function main(){
 const request=JSON.parse(fs.readFileSync(0,'utf8'));
 if(!Array.isArray(request)||request.length>2000)err('invalid batch');
 process.stdout.write(JSON.stringify(request.map(evaluate))+'\n');
}
if(require.main===module)main();
module.exports={runPortable,evaluate,binary,pythonFloatString};
