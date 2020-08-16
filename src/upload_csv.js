
const fs = require('fs');
const request = require('request');
const moment = require('moment-timezone');
const mkdirp = require('mkdirp');
require('dotenv').config();

const path = require('path');
const { uploadCSV } = require('./google-uploader');

const DATA_DIR = './data';

const main = async () => {
  for (let i = 5; i >= 0; i--) {
    const date = moment().add(- i, 'day').format('YYYY-MM-DD');
    const dateDir = path.join(DATA_DIR, date);
    if (!fs.existsSync(dateDir)) {
      continue;
    }

    const buildingListEn = path.join(dateDir, 'building_list_en.csv');

    try {
      await uploadCSV(buildingListEn, {
        spreadsheetId: process.env.SPREADSHEET_ID,
        sheetName: date,
        columnMap: [
          1, 9, 1, 1, 2
        ],
        headers: [
          'enabled',
          'case_no',
          'start_date',
          'start_time_period',
          'end_date', 'type',
          'sub_district_zh', ' ', 'location_zh',
          'location_en', 'action_zh', 'action_en',
          'remarks_zh', 'remarks_en', 'lat', 'lng',
          'source_url_1', 'source_url_2', 'source_file_date', 'source_file_type'
        ],        
      });

      const buildingListZh = path.join(dateDir, 'building_list_tc.csv');


      await uploadCSV(buildingListZh, {
        spreadsheetId: process.env.SPREADSHEET_ID,
        sheetName: date,
        columnMap: [
          1, 6, 8, 1, 2
        ],
        headers: [
          'enabled',
          'case_no',
          'start_date',
          'start_time_period',
          'end_date', 'type',
          'sub_district_zh', ' ', 'location_zh',
          'location_en', 'action_zh', 'action_en',
          'remarks_zh', 'remarks_en', 'lat', 'lng',
          'source_url_1', 'source_url_2', 'source_file_date', 'source_file_type'
        ],
      });
    } catch (error) {
      console.error(`cannot upload ${date}`);
      console.error(error);
    }
  }

}

main()
  .then(() => {
    process.exit(0);
  })
  .catch((err) => {
    console.error(err);
  })