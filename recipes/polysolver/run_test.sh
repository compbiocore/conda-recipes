#!/bin/bash

# stop on the first error
set -eu -o pipefail

export _JAVA_OPTIONS="-Xmx2g"

echo "Testing shell_call_hla_type"
shell_call_hla_type test/test.bam Unknown 1 hg19 STDFQ 0 test

# this test takes too long, have to do manually
#echo "Testing shell_call_hla_mutations_from_type"
#shell_call_hla_mutations_from_type test/test.bam test/test.tumor.bam test/orig.winners.hla.txt hg19 STDFQ test

echo "Testing shell_annotate_hla_mutations"
shell_annotate_hla_mutations indiv output