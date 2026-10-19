"use strict";
// Independent fixed-point cents comparator. No Python imports or SI source parsing.
// Monetary result: round-half-even(price_cents * (10000 + rate_bps) / 10000).
const fs=require("node:fs");
function money(price,rate){
 if(!/^(?:0|[1-9][0-9]{0,6})\.[0-9]{2}$/.test(price) ||
    !/^(?:0|1)\.[0-9]{1,4}$/.test(rate))throw Error("invalid input");
 const [whole,cent]=price.split(".");
 const [rwhole,rfrac]=rate.split(".");
 const cents=BigInt(whole)*100n+BigInt(cent);
 const bps=BigInt(rwhole)*10000n+BigInt(rfrac.padEnd(4,"0"));
 if(cents>100000000n || bps>10000n)throw Error("out of bounds");
 const scaled=cents*(10000n+bps);
 const quotient=scaled/10000n,remainder=scaled%10000n;
 const rounded=quotient+(2n*remainder>10000n ||(2n*remainder===10000n && (quotient&1n)===1n)?1n:0n);
 return (rounded/100n).toString()+"."+(rounded%100n).toString().padStart(2,"0");
}
function main(){
 const items=JSON.parse(fs.readFileSync(0,"utf8"));
 if(!Array.isArray(items)||items.length>1000)throw Error("invalid batch");
 process.stdout.write(JSON.stringify(items.map(x=>money(x.price,x.rate)))+"\n");
}
if(require.main===module)main();
module.exports={money};
