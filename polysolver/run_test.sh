#!/bin/bash

$PREFIX/bin/shell_call_hla_type test/test.bam Unknown 1 hg19 STDFQ 0 test
$PREFIX/bin/shell_call_hla_mutations_from_type test/test.bam test/test.tumor.bam test/winners.hla.txt hg19 STDFQ test