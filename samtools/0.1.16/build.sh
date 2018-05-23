#!/bin/sh
sed -i.bak 's/-lcurses/-lncurses -ltinfo/' Makefile
make
mkdir -p $PREFIX/bin
mv samtools $PREFIX/bin
mkdir -p $PREFIX/lib
mv libbam.a $PREFIX/lib