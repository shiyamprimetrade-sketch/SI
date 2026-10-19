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
 // Match the common Python shortest-decimal repr convention, using the
 // JavaScript binary64 shortest decimal as the seed.
 if(!Number.isFinite(n))err('non-finite numeric result');
 if(Object.is(n,-0))return '-0.0';
 if(n===0)return '0.0';
 const sign=n<0?'-':'';
 const raw=String(Math.abs(n)).toLowerCase();
 const [mantissa,exponentString]=raw.split('e');
 const e=exponentString===undefined?0:Number(exponentString);
 const point=mantissa.indexOf('.');
 let digits=mantissa.replace('.','');
 let power=e-(point<0?0:mantissa.length-point-1);
 digits=digits.replace(/^0+/,'');
 while(digits.length>1&&digits.endsWith('0')){digits=digits.slice(0,-1);power++;}
 const decimalExponent=digits.length-1+power;
 if(decimalExponent>=16||decimalExponent< -4){
   const coefficient=digits[0]+(digits.length>1?'.'+digits.slice(1):'');
   const exp=(decimalExponent>=0?'+':'-')+String(Math.abs(decimalExponent)).padStart(2,'0');
   return sign+coefficient+'e'+exp;
 }
 const placement=digits.length+power;
 if(placement<=0)return sign+'0.'+'0'.repeat(-placement)+digits;
 if(placement>=digits.length)return sign+digits+'0'.repeat(placement-digits.length)+'.0';
 return sign+digits.slice(0,placement)+'.'+digits.slice(placement);
}
function fmt(x){check(x);return x.kind==='int'?x.value.toString():pythonFloatString(x.value);}
function toFloat(x){
 if(x.kind==='float')return x.value;
 const n=Number(x.value);
 if(!Number.isFinite(n))err('numeric overflow');
 return n;
}
// Directly round an arbitrary BigInt ratio to IEEE-754 binary64.
function rationalDivide(a,b){
 if(b===0n)err('division by zero');
 const negative=(a<0n)!==(b<0n);
 let A=a<0n?-a:a,B=b<0n?-b:b;
 if(A===0n)return negative?-0:0;
 const bits=x=>x.toString(2).length;
 let exponent=bits(A)-bits(B);
 if(exponent>=0){
   if(A<(B<<BigInt(exponent)))exponent--;
 }else if((A<<BigInt(-exponent))<B)exponent--;
 if(exponent>1023)err('numeric overflow');
 const round=(n,d)=>{
   const q=n/d,r=n%d,twice=r*2n;
   return q+(twice>d||(twice===d&&(q&1n)===1n)?1n:0n);
 };
 let significand,biased;
 if(exponent< -1022){
   if(exponent< -1075)return negative?-0:0;
   significand=round(A<<1074n,B);
   biased=significand===(1n<<52n)?1n:0n;
   if(biased)significand=0n;
 }else {
   const shift=52-exponent;
   significand=shift>=0?round(A<<BigInt(shift),B):round(A,B<<BigInt(-shift));
   if(significand===(1n<<53n)){significand>>=1n;exponent++;}
   if(exponent>1023)err('numeric overflow');
   biased=BigInt(exponent+1023);
   significand-=(1n<<52n);
 }
 const raw=(negative?(1n<<63n):0n)|(biased<<52n)|significand;
 const bytes=new ArrayBuffer(8),dv=new DataView(bytes);
 dv.setBigUint64(0,raw,false);
 return dv.getFloat64(0,false);
}
function floatFraction(value){
 const buf=new ArrayBuffer(8),dv=new DataView(buf);
 dv.setFloat64(0,value,false);
 const bits=dv.getBigUint64(0,false);
 const sign=(bits>>63n)?-1n:1n;
 const exponent=Number((bits>>52n)&2047n);
 let numerator=bits&((1n<<52n)-1n);
 const power=exponent===0?-1074:exponent-1023-52;
 if(exponent!==0)numerator|=(1n<<52n);
 numerator*=sign;
 if(power>=0)return [numerator<<BigInt(power),1n];
 return [numerator,1n<<BigInt(-power)];
}
function compareNumeric(a,b){
 if(a.kind==='int'&&b.kind==='int')return a.value===b.value?0:a.value<b.value?-1:1;
 if(a.kind==='float'&&b.kind==='float')return a.value===b.value?0:a.value<b.value?-1:1;
 const [n,d]=floatFraction(a.kind==='float'?a.value:b.value);
 const integer=a.kind==='int'?a.value:b.value;
 const relation=integer*d===n?0:integer*d<n?-1:1;
 return a.kind==='int'?relation:-relation;
}
function nonZero(x){return x.kind==='int'?x.value!==0n:x.value!==0;}
function binary(op,a,b){
 check(a);check(b);
 const ints=a.kind==='int'&&b.kind==='int';
 if(op==='EQ'||op==='LT'){
   const comparison=compareNumeric(a,b);
   return int(op==='EQ'?(comparison===0?1:0):(comparison<0?1:0));
 }
 if(op==='DIV'){
   if(!nonZero(b))err('division by zero');
   if(ints)return check(flt(rationalDivide(a.value,b.value)));
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
module.exports={runPortable,evaluate,binary,pythonFloatString,rationalDivide,compareNumeric};
