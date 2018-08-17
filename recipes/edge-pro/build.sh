#!/bin/bash
rm count
make
mkdir -p $PREFIX/bin
cp count edge.pl additionalScripts/addColumns.perl additionalScripts/edgeToDeseq.perl $PREFIX/bin/
