const fs = require('fs');
const request = require('request');
const moment = require('moment-timezone');
const mkdirp = require('mkdirp');
const path = require('path');
const pdfParser = require('./pdf-parser');

// https://www.chp.gov.hk/files/pdf/building_list_chi.pdf
// https://www.chp.gov.hk/files/pdf/building_list_eng.pdf
// https://www.chp.gov.hk/files/pdf/flights_trains_tc.pdf
// https://www.chp.gov.hk/files/pdf/flights_trains_en.pdf



const transformLocalSituation = async (fromPDFFile, toCSVFile) => {
  try {
    const rows = await pdfParser.parseFile(fromPDFFile, {
      cmd: 'GRID'
    });
    console.log(rows.filter((_,i) => i < 10));
    const csv = rows
      .filter(cols => cols.length > 0)
      // get rid of headers
      .filter((cols, index) => index === 0 || (cols[0] && cols[0].text.match(/^\d+$/)))
      .map(cols => cols.map(col => escapeCsv(col.text)).join(',')).join('\n')
    fs.writeFileSync(toCSVFile, csv);
  } catch (error) {
    console.error(`error when transforming local situation pdf.. error: ${error}`);
  }
  
}

function escapeCsv(text) {
  return `"${text.replace('"', '\\"')}"`;
}

module.exports = {
  transformLocalSituation,
}