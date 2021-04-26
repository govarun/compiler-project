nasm -f elf32 $1
filename=$(echo $1 | sed 's/.asm$/.o/g')
gcc -m32 -no-pie $filename
./a.out
echo $?