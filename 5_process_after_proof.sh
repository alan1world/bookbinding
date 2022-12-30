#! /bin/bash

# mkdir ghost - this should now be created in the compile section
# add html header text 

cd "../3. text review"

# find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} ./charm \;
find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} ./ghost \;

# The ghostwriter html output file should have been saved in the ghost folder
#  and the source md file stays in the Text Review folder
cd ghost/
cat '/mnt/Store1/root/Scans/To Be Processed/3. To be formatted/text_to_add_to_ghost.txt' > ghost.html
cat out.html >> ghost.html
cat '/mnt/Store1/root/Scans/To Be Processed/3. To be formatted/text_to_end_ghost.txt' >> ghost.html
cd ../

# mkdir process
# mkdir process/Pandoc
find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} "../4. outputs/Pandoc" \;
find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} "../4. outputs/html" \;
find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} "../4. outputs/LaTex" \;
find . -maxdepth 1 -type d -iname "*_files" -exec cp -r {} "../5. prepress" \;
echo "Starting PDF creation"
pandoc --standalone -f markdown --pdf-engine=xelatex -o "../4. outputs/Pandoc/pandoc.pdf" out.md
echo "Starting HTML creation"
pandoc --standalone -f markdown -t html+smart -o "../4. outputs/Pandoc/pandoc.html" out.md
echo "Starting LaTex creation"
pandoc --standalone -f markdown -t latex -o "../4. outputs/Pandoc/pandoc.tex" out.md

cd "../4. outputs/"
cp Pandoc/pandoc.html html/out.html
cp Pandoc/pandoc.tex LaTex/pandoc.tex
cd LaTex

echo "Converting LaTex file to ASCII"
iconv -c -t iso-8859-1 < pandoc.tex > in.tex
iconv -c -t UTF-8 < in.tex > out.tex
echo "Running LaTex now"
pdflatex -interaction nonstopmode -file-line-error out.tex
cd ..
cd ..

git add *
git commit -m "After proofing"
