#!/bin/bash

echo "Checking for docuntantation changes..."

DOC_CHANGES=$(git diff --cached --name-only --diff-filter=ACM | grep docs/ | wc -l | sed 's/^ *//g')

if [ $DOC_CHANGES -gt 0 ]
then
    echo "$DOC_CHANGES doc files changed. Deploying to github pages..."
    poetry run mkdocs gh-deploy
else
    echo "No new changes to deploy!"
fi