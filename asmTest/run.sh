nasm -f elf64 $1
filename=$(echo $1 | sed 's/.asm$/.o/g')
gcc -m64 -no-pie $filename
./a.out
echo $?