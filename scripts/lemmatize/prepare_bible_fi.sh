#!/bin/sh

mkdir -p ./temp/fi
rm ./temp/fi/*
source=https://raw.githubusercontent.com/Beblia/Holy-Bible-XML-Format/edc4c6fddf711a7bd97e248536b746cdc7fa549f/Finnish1992Bible.xml
curl $source > ./temp/fi/bible_fi.xml

# filter only verses | strip all xml tags | strip extra whitespace
grep "verse" ./temp/fi/bible_fi.xml | sed -e 's/<[^>]*>//g' | awk '{$1=$1};1' > ./temp/fi/bible_fi.txt
