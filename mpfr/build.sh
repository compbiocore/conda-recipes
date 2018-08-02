#!/bin/bash

export LD_LIBRARY_PATH=$PREFIX/lib
export LIBRARY_PATH=$PREFIX/lib
export LDFLAGS="${LDFLAGS} -L${PREFIX}/lib"

./configure --prefix=$PREFIX \
            --with-gmp=$PREFIX \
            --enable-static
make
#make check
make install
