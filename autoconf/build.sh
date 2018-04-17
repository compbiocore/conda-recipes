#!/bin/sh

./configure --prefix=$PREFIX PERL='/usr/bin/perl'

make
#make check
make install

