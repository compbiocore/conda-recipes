#!/bin/sh

export CFLAGS="-I$PREFIX/include"
export LDFLAGS="-L$PREFIX/lib"
./configure --prefix=$PREFIX   \
            --with-internal-glib

make
make install
