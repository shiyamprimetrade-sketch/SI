"use strict";
/* Independent, narrowly scoped JS v0.25 relational source evaluator.
   Supports the documented fixed workflow only; rejects other AxiomFlow
   constructs. Arithmetic uses integer cents and ties-to-even, no Python. */
const fs=require("node:fs");
function cents(text) {
 if(typeof text!=="string"||!/^(?:0|[1-9][0-9]{0,6})\.[0-9]{2}$/.test(text))
  throw Error("invalid USD literal");
 const parts=text.split(".");
 return BigInt(parts[0])*100n+BigInt(parts[1]);
}
function decimal(n){
 if(n<0n)throw Error("negative result unsupported");
 return (n/100n).toString()+"."+(n%100n).toString().padStart(2,"0")+" USD";
}
function roundRatio(n,d){
 let q=n/d,r=n%d;
 return q+(2n*r>d||(2n*r===d&&(q&1n)===1n)?1n:0n);
}
function execute(source,values){
 if(typeof source!=="string"||source.length>10000||!Array.isArray(values)||values.length>500)
  throw Error("invalid bounded input");
 const lines=source.split(/\r?\n/).map(s=>s.split("#")[0].trim()).filter(Boolean);
 if(lines.length>100)throw Error("statement budget");
 let state=null,output=[],schema=["price_usd","rate","observed_cost_usd"],count=0;
 for(const line of lines){
  if(/^table t = input$/.test(line)){
   if(state!==null)throw Error("duplicate table");
   state=values.map(row=>{
    if(!Array.isArray(row)||row.length!==3)throw Error("invalid CSV row");
    const p=cents(row[0]);
    if(!/^(?:0|1)\.[0-9]{1,4}$/.test(row[1]))throw Error("bad rate");
    const rate=BigInt(row[1].split(".")[0])*10000n+
      BigInt(row[1].split(".")[1].padEnd(4,"0"));
    if(rate>10000n)throw Error("rate bound");
    return {price_usd:p,rate,observed_cost_usd:cents(row[2])};
   });
  }else if(state===null)throw Error("table input required");
  else {
   let m;
   if((m=/^filter t where price_usd >= ((?:0|[1-9][0-9]{0,6})\.[0-9]{2}) USD$/.exec(line))){
    const threshold=cents(m[1]);state=state.filter(row=>row.price_usd>=threshold);
   }else if(/^derive t adjusted_usd = price_usd \* 1\.10$/.test(line)){
    if(schema.includes("adjusted_usd"))throw Error("duplicate column");
    state=state.map(row=>({...row,adjusted_usd:roundRatio(row.price_usd*110n,100n)}));
    schema=[...schema,"adjusted_usd"];
   }else if(/^sort t by price_usd$/.test(line)){
    state=state.slice().sort((a,b)=>a.price_usd<b.price_usd?-1:a.price_usd>b.price_usd?1:0);
   }else if(/^sum t\.adjusted_usd$/.test(line)){
    if(!schema.includes("adjusted_usd"))throw Error("undefined derived column");
    let total=state.reduce((acc,row)=>acc+row.adjusted_usd,0n);
    output.push({operation:"sum",column:"adjusted_usd",value:decimal(total)});
   }else if(/^select t \(price_usd\s*,\s*adjusted_usd\)$/.test(line)){
    if(!schema.includes("adjusted_usd"))throw Error("missing column");
    schema=["price_usd","adjusted_usd"];
   }else if(/^emit t$/.test(line)){
    output.push({operation:"emit",columns:schema.slice(),
     types:schema.map(x=>x==="rate"?"scalar":"USD"),
     rows:state.map(row=>schema.map(key=>key==="rate"
       ?(row.rate/10000n).toString()+"."+(row.rate%10000n).toString().padStart(4,"0")
       :decimal(row[key])))});
   }else throw Error("unsupported reference statement");
  }
  count++;
 }
 if(!output.length)throw Error("no output");
 return output;
}
function main(){
 const batch=JSON.parse(fs.readFileSync(0,"utf8"));
 if(!Array.isArray(batch)||batch.length>500)throw Error("invalid batch");
 process.stdout.write(JSON.stringify(batch.map(x=>execute(x.source,x.rows)))+"\n");
}
if(require.main===module)main();
module.exports={execute};
