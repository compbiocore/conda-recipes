#!/bin/bash

# libpll libraries
cp $RECIPE_DIR/libpll-1.0.2-sse3-64.tar.gz $SRC_DIR
tar -zxf $SRC_DIR/libpll-1.0.2-sse3-64.tar.gz

mkdir build && cd build
cmake .. -DCMAKE_LIBRARY_PATH="$SRC_DIR/libpll-1.0.2-sse3-64" -DCMAKE_INCLUDE_PATH="$SRC_DIR/libpll-1.0.2-sse3-64/include/" -DBOOST_ROOT="$SRC_DIR/boost" -DCMAKE_INSTALL_PREFIX:PATH="${PREFIX}"
make install