#!/bin/sh
sed -i.bak 's/-lcurses/-lncurses -ltinfo/g' Makefile
sed -i.bak 's/-D_CURSES_LIB=1/-D_CURSES_LIB=0/g' Makefile
cat Makefile
make
mkdir -p $PREFIX/bin
mv samtools $PREFIX/bin
mkdir -p $PREFIX/lib
mv libbam.a $PREFIX/lib