python3 ./src/main.py "$1" > /dev/null
if [ $? -gt 0 ]
then
    exit
fi
./run_test.sh out.asm