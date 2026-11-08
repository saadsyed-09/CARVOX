const fs=require('fs');const path=require('path');
fs.rmSync('www',{recursive:true,force:true});fs.mkdirSync('www/assets',{recursive:true});
fs.copyFileSync('index.html','www/index.html');
for(const name of ['carvox-logo.png','icon.png']){const p=path.join('assets',name);if(fs.existsSync(p))fs.copyFileSync(p,path.join('www/assets',name));}
console.log('CARVOX web build ready');
