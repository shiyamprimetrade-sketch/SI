"use strict";
// Independent bounded fixed-point table comparison, not a complete AxiomFlow JS runtime.
const fs=require("node:fs");
function cents(text){
 if(typeof text!=="string" || !/^(?:0|[1-9][0-9]{0,6})\.[0-9]{2}$/.test(text))throw Error("invalid cents");
 const [a,b]=text.split(".");
 return BigInt(a)*100n+BigInt(b);
}
function display(value){
 return (value/100n).toString()+"."+(value%100n).toString().padStart(2,"0")+" USD";
}
function round110(c){
 const v=c*110n,q=v/100n,r=v%100n;
 return q+(r>50n || (r===50n && (q&1n)===1n)?1n:0n);
}
function run(batch){
 if(!Array.isArray(batch)||batch.length>500)throw Error("invalid batch");
 return batch.map(({minimum,rows})=>{
  if(!Array.isArray(rows)||rows.length>500)throw Error("invalid rows");
  const min=cents(minimum);
  const items=rows.map(cents).filter(x=>x>=min).map(x=>[x,round110(x)]);
  const sum=items.reduce((a,x)=>a+x[1],0n);
  return {sum:display(sum),rows:items.map(x=>[display(x[0]),display(x[1])])};
 });
}
if(require.main===module){
 process.stdout.write(JSON.stringify(run(JSON.parse(fs.readFileSync(0,"utf8"))))+"\n");
}
module.exports={run};
