python3 src/main.py "$1" 2> /dev/null
if [ $? -gt 0 ]
then
    exit
fi
printf "\n-----Program Output-----\n"
./run.sh out.asm
printf "\n------------------------"