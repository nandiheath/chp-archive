# CHP PDF Archive Repo

This repository archives the official released pdfs (mostly from chp.gov.hk) and convert them to csv. They are as the references for [wars.vote4.hk](https://wars.vote4.hk) and keep as historical records.

And this repository will publish to [github pages](https://nandiheath.github.io/chp-archive/) for external party referencing the materials.

## Setup

For downloading the pdfs

```bash
yarn run download
```

For running the csv convertor

```bash
cd data

python extract_chp_share_case.py
```

For generating the html

```bash
yarn run publish
```

For uploading the csv to google spreadsheet

```bash
yarn run upload
```

## Contributions

Thanks [rowena-sc-lai](https://github.com/rowena-sc-lai) for making the pdf to csv converter and helping to keep the archive files consistent if the jobs failed.
