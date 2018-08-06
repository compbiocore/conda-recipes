#!/bin/bash
# Make sure pipes to tee don't hide configuration or test failures
set -o pipefail

export C_INCLUDE_PATH=${PREFIX}/include

# build system needs samtools source files
wget http://depot.galaxyproject.org/package/source/samtools/samtools-0.1.16.tar.bz2
tar xjf samtools-0.1.16.tar.bz2 && cd samtools-0.1.16
mv ${PREFIX}/lib/libbam.a ./

# tell build system where libbam.a and bam.h (and other files) are
export SAMTOOLS=$PWD

cd ../

# If it has Build.PL use that, otherwise use Makefile.PL
if [ -f Build.PL ]; then
    perl Build.PL 2>&1 | tee configure.log
    perl ./Build
    perl ./Build test 2>&1 | tee tests.log
    # Make sure this goes in site
    perl ./Build install --installdirs site
elif [ -f Makefile.PL ]; then
    # Make sure this goes in site
    perl Makefile.PL INSTALLDIRS=site
    make
    make test 2>&1
    make install
else
    echo 'Unable to find Build.PL or Makefile.PL. You need to modify build.sh.'
    exit 1
fi

# https://github.com/conda/conda-build/issues/2824
for i in $(ls blib/script); do
    chmod u+w $PREFIX/bin/$i
done