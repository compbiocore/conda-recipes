#!/usr/bin/env sh
R CMD javareconf > /dev/null 2>&1 || true
R --vanilla -e 'install.packages("curl", repos="http://cran.mtu.edu")'

