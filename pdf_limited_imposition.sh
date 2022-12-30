#! /usr/bin/env bash
# -*- coding: utf-8 -*-

set -e

INPUT="$1"
BASE_INPUT=$(basename "$1" .pdf)
# TOTAL=`pdftk file.pdf dump_data | grep NumberOfPages | awk '{print $2}'` 
TOTAL=`pdftk $INPUT dump_data | grep NumberOfPages | awk '{print $2}'` 

# if (( $TOTAL % 4 == 0 ))
# then
	# echo "Your number is divisible by 5"
	# $TOTAL4
# else
	# echo "Your number is not divisible by 5"
# fi

# TOTAL4=$(( $TOTAL / 4 ))
echo "Pages: "$TOTAL
# echo $TOTAL4

mkdir -p $BASE_INPUT-seperated
mkdir -p $BASE_INPUT-merged

for i in `seq 1 4 $TOTAL`
do 
	# check if total - i is less than 4, if so use the remainder
	REMAINDER=$(( $TOTAL + 1 - i ))
	echo $REMAINDER
	if (( $REMAINDER < 4 ))
	then
		j=$TOTAL
	else
		j=$((i+3))
	fi
	echo "pdftk $INPUT cat $i-$j output $INPUT-seperated\output_$i-$j.pdf"
	pdftk $INPUT cat $i-$j output $BASE_INPUT-seperated/output_$i-$j.pdf
done

for f in $BASE_INPUT-seperated/*.pdf
do
	echo $f
	BASE_FILE=$(basename "$f")
	# echo $BASE_INPUT-merged/$BASE_FILE
	bookletimposer -a -b -p 2x1 -f A4 -o "$BASE_INPUT-merged/$BASE_FILE" $f || true
done

pdfunite $BASE_INPUT-merged/*.pdf $BASE_INPUT-joined.pdf
# pdfunite $(ls -v *.pdf) output.pdf
# pdfunite $(ls *.pdf | sort -n) output.pdf
