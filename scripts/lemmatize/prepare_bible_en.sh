#!/bin/sh

mkdir -p ./temp/en
rm ./temp/en/*
source=https://raw.githubusercontent.com/Beblia/Holy-Bible-XML-Format/f1d25671715588720b7a68c141cd5b6e9774f0cd/EnglishKJBible.xml
curl $source > ./temp/en/bible_en.xml

# filter only verses | strip all xml tags | strip extra whitespace
grep "verse" ./temp/en/bible_en.xml | sed -e 's/<[^>]*>//g' | awk '{$1=$1};1' > ./temp/en/bible_en.txt
