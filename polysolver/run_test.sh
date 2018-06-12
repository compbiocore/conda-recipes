#!/bin/bash

# stop on the first error
set -eu -o pipefail

# test shell_call_hla_type
echo "Testing shell_call_hla_type"
$PREFIX/bin/shell_call_hla_type test/test.bam Unknown 1 hg19 STDFQ 0 test

# test shell_call_hla_mutations_from_type
echo "Testing shell_call_hla_mutations_from_type"
$PREFIX/bin/shell_call_hla_mutations_from_type test/test.bam test/test.tumor.bam test/orig.winners.hla.txt hg19 STDFQ test