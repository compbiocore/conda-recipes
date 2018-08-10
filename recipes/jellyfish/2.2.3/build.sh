#!/bin/bash

pushd $SRC_DIR

autoreconf -i
#./configure --prefix=$PREFIX --disable-Werror
./configure --prefix=$PREFIX CXXFLAGS='-Wno-deprecated-declarations '$CXXFLAGS
make
make install
#make check
