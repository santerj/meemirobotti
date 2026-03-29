#!/bin/sh

mkdir -p morpho
curl https://www.puimula.org/htp/testing/voikko-snapshot-v5/dict-morpho.zip -o morpho/dict-morpho.zip
unzip morpho/dict-morpho.zip -d morpho/
rm morpho/dict-morpho.zip
