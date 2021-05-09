#!/bin/bash

if [ $# -eq 1]; do
    cd ./"$1"
done

for file in *; do
    gcc "$file"
    ./a.out > gccOutput.txt
    ./compile_test.sh "$file"
    echo "------------ Testing: $file ------------"
    diff gccOutput.txt codeOutput.txt
    rm a.out gccOutput.txt codeOutput.txt
done
