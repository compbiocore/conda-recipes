#!/bin/bash
set -eu -o pipefail

outdir=$PREFIX/share/$PKG_NAME=$PKG_VERSION-$PKG_BUILDNUM
mkdir -p $outdir
#mkdir -p $PREFIX/bin
#cp -R * $outdir/
cp $RECIPE_DIR/bin/muTect-1.1.6.jar $outdir/muTect-1.1.6.jar
cp $RECIPE_DIR/mutect.py $outdir/mutect
ls -l $outdir
ln -s $outdir/mutect $PREFIX/bin
chmod 0755 "${PREFIX}/bin/mutect"