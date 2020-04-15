const PDFParser = require('pdf2json');
const _ = require('lodash');
const chalk = require('chalk');

const OPT_GRID = 'GRID';
const OPT_INDENT = 'INDENT';

const HEADER_Y = 11.0;
const FOOTER_Y = 47.0;

const ROW_THRESHOLD = 1.5;
const COLUMN_THRESHOLD = 10.0;

// sometimes the text overlapped with the lines
const CELL_OFFSET_H = 0.05;

function groupColumn(text) {
  const { x } = text;
  if (x < 17) return '0';
  if (x < 20) return '1';
  if (x < 27) return '2';
  if (x < 30) return '3';
  return 4;
}

function parsePages(pages, options) {
  if (options.cmd === OPT_GRID) {
    return parsePagesWithGrid(pages, options);
  } else {
    return parsePagesWithIndent(pages, options);
  }
}

function parsePagesWithIndent(pages) {
  console.log(chalk.yellow(`Total ${pages.length} pages ..`)
  );
  const outputPages = [];
  for (const page of pages) {
    const ungroupedTexts = [];
    for (const text of page.Texts) {
      // drop all the headers
      if (text.y < HEADER_Y || text.y > FOOTER_Y) {
        continue;
      }
      ungroupedTexts.push(text);
    }

    let rows = _.groupBy(ungroupedTexts, text => `${Math.round(text.y / ROW_THRESHOLD, 2)}`);
    rows = Object.values(rows)
      .map(row => _.groupBy(row, groupColumn))
      .map(row => Object.values(row).map(
        columns => columns.map(
          column => ({
            x: column.x,
            bold: column.R.map(r => r.TS[2]).reduce((c, v) => Math.max(c, v), 0),
            text: column.R.map(r => decodeURIComponent(r.T)).join(''),
          }),
        ),
      ));

    outputPages.push(rows);
  }

  // Grouped pages with row and column
  return _.flatten(outputPages);
}

function parsePagesWithGrid(pages) {
  console.log(chalk.yellow(`Total ${pages.length} pages ..`)
  );
  const outputPages = [];
  for (const page of pages) {
    let row = -1;
    let lastY = 0;
    let grids = [];
    let cols = [];
    // So the fills here is the lines
    for (const fill of page.Fills) {
      const { x, y, w, h } = fill;
      // only count the horizontal lines
      if (h > 1 || w < 1) {
        continue;
      }
      fill.row = row;
      if (y > lastY) {
        row++;
        // try to get the header (in a hacky way)
        if (y - lastY < 4) {
          grids.push(...cols.map((col, index) => ({
            x: col.x,
            y: col.y,
            w: col.w,
            h: y - lastY,
            col: index,
            row,
          })));
        }
        lastY = y

        cols = [];
      }
      cols.push({
        x, y, w
      })
    }
    const rows = _.times(grids.length, () => [])
    let xy = 0

    for (const text of page.Texts) {
      const { x, y, R } = text;

      for (let i = xy; i < grids.length; i++) {
        const fill = grids[i];
        // Do it in seqential order so we wont miss the grid
        if (x >= fill.x && x <= (fill.x + fill.w) &&
          y >= fill.y - CELL_OFFSET_H && y <= (fill.y + fill.h - CELL_OFFSET_H)) {
          // within the rect
          if (rows[fill.row][fill.col] === undefined) {
            rows[fill.row][fill.col] = [];
          }
          rows[fill.row][fill.col].push({
            bold: R.map(r => r.TS[2]).reduce((c, v) => Math.max(c, v), 0),
            text: R.map(r => decodeURIComponent(r.T)).join(''),
          })
          break;

        }
      }
    }
    outputPages.push(rows.map(row => row.map(col => col.reduce((c, v) => ({ bold: c.bold, text: c.text + v.text }), { bold: 0, text: '' }))));
  }

  // Grouped pages with row and column
  return _.flatten(outputPages);
}



module.exports = {
  parseFile: (filePath, options) => (new Promise((resolve, reject) => {
    // pdf is downloaded
    const pdfParser = new PDFParser(this);
    pdfParser.on('pdfParser_dataError', (errData) => {
      console.error(errData);
      reject(errData);
    });
    pdfParser.on('pdfParser_dataReady', (pdfData) => {
      const pages = pdfData.formImage.Pages;
      const formattedData = parsePages(pages, options);
      resolve(formattedData);
    });

    pdfParser.loadPDF(filePath);
  })),
};
