#!/bin/bash

# for Linux
    # Boost wants to enable `float128` support on Linux by default.
    # However, we don't install `libquadmath` so it will fail to find
    # the needed headers and fail to compile things. Adding this flag
    # tells Boost not to support `float128` and avoids this search
    # process. As it has confused a few people. We have added it here.
    # The idea to add this flag was inspired by this Boost ticked.
    #
    # https://svn.boost.org/trac/boost/ticket/9240
    #
export CXXFLAGS="${CXXFLAGS} -DBOOST_MATH_DISABLE_FLOAT128"
export LDFLAGS="${LDFLAGS} -Wl,-rpath,${PREFIX}/lib -I${PREFIX}/lib" 
export LINKFLAGS="${LDFLAGS}"
export CPPFLAGS="${CPPFLAGS} -I${PREFIX}/include"
