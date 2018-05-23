#!/bin/bash
wget http://depot.galaxyproject.org/package/source/samtools/samtools-0.1.16.tar.bz2
tar xjf samtools-0.1.16.tar.bz2 && cd samtools-0.1.16
#make CFLAGS="-fPIC -lncurses -ltinfo"
sed -i.bak 's/-lcurses/-lncurses -ltinfo/' Makefile
make CFLAGS="-fPIC"
#export SAMTOOLS=`pwd`
export SAMTOOLS=$PWD
#cpanm Bio::DB::Sam

# Make sure pipes to tee don't hide configuration or test failures
set -o pipefail

export C_INCLUDE_PATH=${PREFIX}/include

# Tell the build system where to find samtools
#export SAMTOOLS="${PREFIX}"

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
