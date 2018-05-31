#!/bin/bash
set -eu -o pipefail

outdir=$PREFIX/share/$PKG_NAME=$PKG_VERSION-$PKG_BUILDNUM
mkdir -p $outdir
cp -R * $outdir/
#mkdir -p $PREFIX/bin

#ls -l $outdir
#cp $SRC_DIR/muTect-1.1.4.jar $PREFIX/jar/muTect-1.1.4.jar