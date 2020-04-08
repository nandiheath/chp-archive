#!/bin/sh
# Credit: https://gist.github.com/willprice/e07efd73fb7f13f917ea

setup_git() {
  git config --global user.email "ci@kintohub.com"
  git config --global user.name "Kinto CI"
}

commit_data() {
  git fetch
  
  git checkout master
  
  git pull

  git status
  # Current month and year, e.g: Apr 2018
  dateAndMonth=`date "+%b %Y"`
  # Stage the modified files in dist/output
  git add -f data

  git add index.html
  # Create a new commit with a custom build message
  # with "[skip ci]" to avoid a build loop
  # and Travis build number for reference
  git commit -m "pushing new pdfs at $dateAndMonth" -m "[skip ci]"    
}

upload_files() {
  git remote add upstream https://nandiheath:${GH_TOKEN}@github.com/nandiheath/chp-archive.git > /dev/null 2>&1
  git push --quiet --set-upstream upstream master
}

setup_git

node run.js

commit_data

# Attempt to commit to git only if "git commit" succeeded
if [ $? -eq 0 ]; then
  echo "A new commit with changed data or index.html . Uploading to GitHub"
  upload_files
else
  echo "No changes. Skip deploying"
fi
