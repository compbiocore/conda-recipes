#!/bin/bash

# skip the creation of man pages by faking existance of help2man
if [ `uname` == Darwin ]; then
    export HELP2MAN=/usr/bin/true
fi
if [ `uname` == Linux ]; then
    export HELP2MAN=/bin/true
fi
./configure --prefix="$PREFIX"
make
make check
make install
