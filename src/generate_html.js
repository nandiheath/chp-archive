const fs = require('fs');
const request = require('request');
const moment = require('moment-timezone');
const mkdirp = require('mkdirp');
const path = require('path');

const generateHtml = () => {
  const folders = fs.readdirSync('data');
  const paths = [];
  folders.forEach(dir => {
    const stat = fs.statSync('data/' + dir);
    if (!stat.isDirectory()) {
      return;
    }
    const dateDir = fs.readdirSync('data/' + dir);
    dateDir.forEach(file => {
      paths.push({
        date: dir,
        file,
        path: `data/${dir}/${file}`
      });
    })
  })

  const html = `<ul>${paths.map(p => `<li><a href="${p.path}">${p.date}/${p.file}</a></li>`).join('')}</ul>`
  fs.writeFileSync('index.html', fs.readFileSync('index.html.template').toString().replace('__TEMPLATE__', html));
}

const run = async () => {
  generateHtml();
}

// don't cache. throw the error to let travis know
run();
