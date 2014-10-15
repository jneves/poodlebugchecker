#! /bin/bash

DIR=`dirname $0`
if [ x$DIR == x ]; then
    DIR="."
fi

cd $DIR/..
python script/poodlebug.py
cd - > /dev/null
