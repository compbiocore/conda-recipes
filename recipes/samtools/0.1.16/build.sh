#!/bin/sh
export C_INCLUDE_PATH=${PREFIX}/include
make
mkdir -p $PREFIX/bin
mv samtools $PREFIX/bin
mkdir -p $PREFIX/lib
mv libbam.a $PREFIX/lib