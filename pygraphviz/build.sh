#!/bin/bash

export CPATH=$PREFIX/include
export LD_RUN_PATH=$PREFIX/lib

pip install --no-deps .
