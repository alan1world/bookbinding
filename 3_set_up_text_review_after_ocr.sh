#!/bin/sh

set -e

cd ..

echo 'Setting up Text Review folder'
cd "2. ocr"
cp -r -t "../3. text review"/ abbyy_files/
cp -t "../3. text review"/ abbyy.htm
cd ../"3. text review"

# html2text2 abbyy.htm > out.md
html2text abbyy.htm > out.md
rm abbyy.htm

cd ..

git add *
git commit -m "After OCR"
