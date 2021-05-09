python3 src/main.py "$1"
if [ $? -gt 0 ]
then
    exit
fi
printf "\n-----Program Output-----\n"
./scripts/run.sh out.asm
printf "\n------------------------"