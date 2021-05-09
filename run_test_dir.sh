#!/bin/bash

# if [ $# -eq 1]; then
#     cd ./"$1"
# fi

for file in "$1"/*; do
    cat template.c > new.c
    cat "$file" >> new.c
    gcc -w new.c
    rm new.c
    ./a.out > gccOutput.txt
    ./compile_test.sh "$file"
    echo "------------ Testing: $file ------------"
    diff gccOutput.txt codeOutput.txt 
    rm a.out gccOutput.txt codeOutput.txt
done
