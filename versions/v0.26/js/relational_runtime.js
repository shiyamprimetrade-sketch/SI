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
 let constants=new Map(),state=null,output=[],schema=["price_usd","rate","observed_cost_usd"],count=0;
 for(const line of lines){
  if(/^let [a-z_][a-z_0-9]* = /.test(line)) {
   if(state!==null||constants.size>=8)throw Error("invalid mixed scope");
   const m=/^let ([a-z_][a-z_0-9]*) = ((?:0|[1-9][0-9]{0,6})\.[0-9]{2} USD|(?:0|[1-9][0-9]*)\.[0-9]+)$/.exec(line);
   if(!m||constants.has(m[1])||["price_usd","rate","observed_cost_usd","adjusted_usd"].includes(m[1]))
     throw Error("invalid or duplicate mixed literal");
   const money=m[2].endsWith(" USD");
   let value;
   if(money)value=cents(m[2].slice(0,-4));
   else {
    const [w,f]=m[2].split(".");
    if(f.length>4)throw Error("unsupported decimal scale");
    value=BigInt(w)*10000n+BigInt(f.padEnd(4,"0"));
   }
   constants.set(m[1],{money,value});
  }else if(/^table t = input$/.test(line)){
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
   if((m=/^filter t where price_usd >= (.+)$/.exec(line))){
    let threshold;
    if(/^(?:0|[1-9][0-9]{0,6})\.[0-9]{2} USD$/.test(m[1]))threshold=cents(m[1].slice(0,-4));
    else if(constants.has(m[1])&&constants.get(m[1]).money)threshold=constants.get(m[1]).value;
    else throw Error("invalid mixed filter type");
    state=state.filter(row=>row.price_usd>=threshold);
   }else if((m=/^derive t adjusted_usd = price_usd \* (1\.10|[a-z_][a-z_0-9]*)$/.exec(line))){
    if(schema.includes("adjusted_usd"))throw Error("duplicate column");
    let factor;
    if(m[1]==="1.10")factor=11000n;
    else if(constants.has(m[1])&&!constants.get(m[1]).money)factor=constants.get(m[1]).value;
    else throw Error("invalid mixed factor type");
    state=state.map(row=>({...row,adjusted_usd:roundRatio(row.price_usd*factor,10000n)}));
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
