
const fs = require('fs');
const request = require('request');
const moment = require('moment-timezone');
const mkdirp = require('mkdirp');
require('dotenv').config();

const path = require('path');
const { uploadCSV } = require('./google-uploader');

const DATA_DIR = './data';

const main = async () => {
  const yesterday = moment().add(-2, 'day').format('YYYY-MM-DD');
  const yesterdayDir = path.join(DATA_DIR, yesterday);
  if (!fs.existsSync(yesterdayDir)) {
    console.error('The file for yesterday does not ready yet.')
    process.exit(0);
  }

  const buildingListEn = path.join(yesterdayDir, 'building_list_en.csv');

  await uploadCSV(buildingListEn, {
    spreadsheetId: process.env.SPREADSHEET_ID,
    sheetName: yesterday
  });
}

main()
  .then(() => {
    process.exit(0);
  })
  .catch((err) => {
    console.error(err);
  })