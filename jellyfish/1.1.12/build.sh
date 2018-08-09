#!/bin/bash

pushd $SRC_DIR

sed -i.bak 's/AM_CXXFLAGS = -g -O3/AM_CXXFLAGS = -g -O3/' Makefile.am
autoreconf -i
./configure --prefix=$PREFIX  
#./configure --prefix=$PREFIX CXXFLAGS='-Wno-deprecated-declarations '$CXXFLAGS
make
make install
make check
