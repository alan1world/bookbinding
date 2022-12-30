#!/bin/sh

set -e

cd ..

echo 'Scanned source files should be in "1. source"'

cd "1. source"

echo 'Starting original cbz creation ...'
find . -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.bmp" -o -iname "*.jpeg" -o -iname "*.jpg" -o -iname "*.tif" -o -iname "*.tiff" \) -exec patool create original.cbz "{}" > /dev/null +
mv -t ../ original.cbz 

# create the reference files
cd out/
echo 'Starting reference cbz creation ...'
patool create reference.cbz *.tif > /dev/null
mv reference.cbz ../../

# Convert all tif files to pdf for individual pages
for f in *.tif; do tiff2pdf -n -z -o $f.pdf $f ; done

# Use libpoppler (pdfunite) or pdftk to merge all pdf files together
pdfunite *.pdf compiled.pdf

echo 'Converting PDF to DJVU ...'
pdf2djvu -o compiled.djvu compiled.pdf

mv compiled.djvu ../../
mv compiled.pdf ../../
rm *.pdf
cd ../../

git add *
git commit -m "After ScanTailor"
