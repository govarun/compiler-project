# nasm -fmacho $1
# filename=$(echo $1 | sed 's/.asm$/.o/g')
# clang++ -arch i386 -Wall -g  -c $filename
# ./a.out
# echo '\n'


# nasm -fmacho out.asm && ld -macosx_version_min 11.2.2 -o a.out out.o && ./simple


nasm -f elf32 $1
filename=$(echo $1 | sed 's/.asm$/.o/g')
x86_64-elf-gcc -m32 -no-pie $filename
./a.out
echo "\n"