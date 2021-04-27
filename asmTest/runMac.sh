nasm -fmacho $1
filename=$(echo $1 | sed 's/.asm$/.o/g')
gcc -arch i386 -no-pie $filename
./a.out
echo '\n'


# nasm -fmacho out.asm && ld -macosx_version_min 11.2.2 -o a.out out.o && ./simple