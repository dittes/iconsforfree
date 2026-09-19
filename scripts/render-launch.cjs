const fs=require('fs');const path=require('path');const sharp=require('sharp');
(async()=>{for(const name of fs.readdirSync('launch/product-hunt').filter(n=>n.endsWith('.svg'))){const dest='launch/product-hunt/'+name.replace('.svg','.png');await sharp('launch/product-hunt/'+name).png().toFile(dest);console.log(dest);}
await sharp('assets/social/preview.svg').png().toFile('assets/social/preview.png');
const tiles=await Promise.all(fs.readdirSync('launch/product-hunt').filter(n=>/^0.*png$/.test(n)).map(async(n,i)=>({input:await sharp('launch/product-hunt/'+n).resize(635,380).toBuffer(),left:(i%2)*635,top:Math.floor(i/2)*380})));
await sharp({create:{width:1270,height:1140,channels:3,background:'#dce3ef'}}).composite(tiles).png().toFile('launch/product-hunt/contact-sheet.png');})().catch(error=>{console.error(error);process.exitCode=1;});
