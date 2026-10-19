// SI v0.11 — independent ECMAScript scanner/parser for SI-Portable-1.
// No Python, no shlex, and no dependency on SI's Python parser.
// Input is one JSON array of source strings, output one JSON array of results.
// This accepts JSON as a transport only; untrusted input requires OS isolation.
'use strict';

const fs = require('node:fs');
const MAX_SOURCE_CHARS = 100000;
const MAX_LITERAL_CHARS = 1200;
const MAX_INTEGER_BITS = 4096;
const MAX_INSTRUCTIONS = 50000;
const LABEL_LIMIT = 64;
const arity = Object.freeze({
  PUSH:1, LABEL:1, JMP:1, JZ:1, ADD:0, SUB:0, MUL:0,
  DIV:0, LT:0, EQ:0, DUP:0, SWAP:0, DROP:0, PRINT:0, HALT:0
});

function fail(message) { throw new Error(message); }
function identifier(value) { return /^[A-Za-z_][A-Za-z0-9_]*$/.test(value) && value.length <= LABEL_LIMIT; }
function lineWords(line) {
  const found = [];
  let word = '';
  for (const ch of line) {
    if (ch === '#') break;
    if (ch === ' ' || ch === '\t') {
      if (word) { found.push(word); word=''; }
    } else { word += ch; }
  }
  if (word) found.push(word);
  return found;
}
function decimal(text, line) {
  if (text.length > MAX_LITERAL_CHARS) fail('line '+line+': integer literal budget exceeded');
  if (!/^[+-]?[0-9]+$/.test(text)) fail('line '+line+': nonportable integer literal');
  const n = BigInt(text);
  const bitLength = (n < 0n ? -n : n).toString(2).replace(/^0$/, '').length;
  if (bitLength > MAX_INTEGER_BITS) fail('integer bit budget exceeded');
  return n.toString(10);
}
function parsePortable(source) {
  if (typeof source !== 'string') fail('source must be a string');
  // SI-Portable-1 text consists entirely of ASCII BMP code units.
  if (source.length > MAX_SOURCE_CHARS) fail('source budget exceeded');
  for (let i=0; i<source.length; i++) {
    const c=source.charCodeAt(i);
    if (!(c>=32 && c<=126) && c!==9 && c!==10 && c!==13)
      fail('nonportable character at offset '+i);
  }
  if (source.replace(/\r\n/g,'').includes('\r')) fail('bare CR line ending is not portable');
  const lines=source.replace(/\r\n/g,'\n').split('\n');
  const labels=new Map();
  const rows=[];
  for(let i=0; i<lines.length; i++){
    const words=lineWords(lines[i]);
    if (!words.length) continue;
    const op=words[0].toUpperCase();
    if (!Object.prototype.hasOwnProperty.call(arity,op)) fail('line '+(i+1)+': unknown opcode '+op);
    if (words.length!==arity[op]+1) fail('line '+(i+1)+': '+op+' needs '+arity[op]+' args');
    const arg=words.length===2?words[1]:null;
    if (['LABEL','JMP','JZ'].includes(op) && !identifier(arg))
      fail('line '+(i+1)+': nonportable label');
    if (op==='LABEL') {
      if (labels.has(arg)) fail('line '+(i+1)+': duplicate label '+arg);
      labels.set(arg,rows.length);
    }
    rows.push({opcode:op,operand:arg,line:i+1});
    if (rows.length>MAX_INSTRUCTIONS) fail('instruction budget exceeded');
  }
  return rows.map(row=>{
    const {opcode,line}=row;
    const operand=opcode==='PUSH'?decimal(row.operand,line):row.operand;
    if ((opcode==='JMP'||opcode==='JZ') && !labels.has(row.operand))
      fail('line '+line+': unknown label '+row.operand);
    return {
      opcode,
      // Integer represented as canonical base-10 string so JSON never loses precision.
      operand,
      target:(opcode==='JMP'||opcode==='JZ')?labels.get(row.operand):null,
      line
    };
  });
}
function canonical(program) {
  return program.map(x=>{
    if (x.opcode==='PUSH') return 'PUSH '+x.operand;
    if (['LABEL','JMP','JZ'].includes(x.opcode)) return x.opcode+' '+x.operand;
    return x.opcode;
  }).join('\n');
}
function evaluateSource(source) {
  try {
    const program=parsePortable(source);
    const norm=canonical(program);
    const second=parsePortable(norm);
    const signature=x=>x.map(y=>[y.opcode,y.operand,y.target]);
    if (JSON.stringify(signature(program))!==JSON.stringify(signature(second)) || canonical(second)!==norm)
      fail('canonical obligation failed');
    return {ok:true,signature:signature(program),canonical:norm};
  } catch(e) {
    return {ok:false,error:String(e.message)};
  }
}
function main() {
  const raw=fs.readFileSync(0,'utf8');
  const input=JSON.parse(raw);
  if(!Array.isArray(input) || input.length>2000) fail('transport input must be an array of at most 2000 sources');
  process.stdout.write(JSON.stringify(input.map(evaluateSource))+'\n');
}
if (require.main===module) main();
module.exports={parsePortable,evaluateSource};
