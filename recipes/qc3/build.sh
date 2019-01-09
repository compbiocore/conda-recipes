#!/bin/bash

# confirm perl modules are installed
bash test.modules

outdir=$PREFIX/share/$PKG_NAME-$PKG_VERSION-$PKG_BUILDNUM
mkdir -p $outdir
mkdir -p $PREFIX/bin
chmod a+x qc3.pl
sed -i.bak 's|#!/user/bin/perl|#!/usr/bin/env perl|g' qc3.pl
sed -i.bak 's|$FindBin::Bin|$FindBin::RealBin|g' qc3.pl
sed -i.bak 's|dirname($0)|$FindBin::RealBin|g' qc3.pl
sed -i.bak '8i use FindBin qw($RealBin);' source/*Summary.pm
sed -i.bak 's|dirname($0)|$RealBin|g' source/*Summary.pm

cp -r * $outdir
ln -s $outdir/qc3.pl $PREFIX/bin