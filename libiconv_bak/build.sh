#!/bin/sh

export CFLAGS="-fPIC $CFLAGS"

./configure --prefix=${PREFIX} \
            --enable-static \
            --disable-rpath

make -j$CPU_COUNT
make check -j$CPU_COUNT
make install -j$CPU_COUNT
