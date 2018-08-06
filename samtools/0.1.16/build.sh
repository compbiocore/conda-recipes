#!/bin/sh
sed -i.bak 's/-lcurses/-lncurses -ltinfo/' Makefile
sed -i.bak 's/-D_CURSES_LIB=1/-D_CURSES_LIB=0/' Makefile
#sed -i 's/curses/ncurses/' bam_tview.c
make 
#$make 
mkdir -p $PREFIX/bin
mv samtools $PREFIX/bin
mkdir -p $PREFIX/lib
mv libbam.a $PREFIX/lib
