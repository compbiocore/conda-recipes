#!/bin/bash

# Download extra sources
#CONDA_PYTHON=$(conda info --root)/bin/python
#${CONDA_PYTHON} ${RECIPE_DIR}/download-extra-sources.py

#ln -s gmp-* gmp
#ln -s mpc-* mpc
#ln -s mpfr-* mpfr
#ln -s isl-* isl

# Install gcc to its very own prefix.
# GCC must not be installed to the same prefix as the environment,
# because $GCC_PREFIX/include is automatically considered to be a
# "system" header path.
# That could cause -I$PREFIX/include to be essentially ignored in users' recipes
# (It would still be on the search path, but it would be in the wrong position in the search order.)

GCC_PREFIX="$PREFIX/gcc"
mkdir "$GCC_PREFIX"
ln -s "$PREFIX/lib" "$PREFIX/lib64"

mkdir -p "${PREFIX}/share"

cat /etc/*-release > "${PREFIX}/share/conda-gcc-build-machine-os-details"
./configure \
        --prefix="$GCC_PREFIX" \
        --with-gxx-include-dir="$GCC_PREFIX/include/c++" \
        --bindir="$PREFIX/bin" \
        --datarootdir="$PREFIX/share" \
        --libdir="$PREFIX/lib" \
        --with-gmp="$PREFIX" \
        --with-mpfr="$PREFIX" \
        --with-mpc="$PREFIX" \
        --with-isl="$PREFIX" \
        --with-cloog="$PREFIX" \
        --enable-checking=release \
        --with-tune=generic \
        --disable-multilib

make -j"$CPU_COUNT"
make install-strip
rm "$PREFIX/lib64"


# Fix libtool paths
find "$PREFIX" -name '*.la' -print0 | xargs -0  sed -i.backup 's%lib/../lib64%lib%g'
find "$PREFIX" -name '*la.backup' -print0 | xargs -0  rm -f


# Link cc to gcc if cc doesn't exist
[ -e "$PREFIX/bin/cc" ] || ln -s "gcc" "$PREFIX/bin/cc"

#./configure \
#  --prefix="$PREFIX" \
#  --with-gxx-include-dir="$GCC_PREFIX/include/c++" \
#  --enable-checking=release \
#  --enable-languages=c,c++,fortran \
#  --disable-multilib

#make -j"$CPU_COUNT"
#make install-strip
