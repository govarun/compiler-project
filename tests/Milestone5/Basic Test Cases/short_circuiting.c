int main(){
    int a = 1, b=5;
    
    if (!printf("first\n") && printf("second\n")){
        ;
    }
    if(printf("third\n") || printf("fourth\n")){
        ;
    }

    if(a || b++){
        printf("Values inside OR If, a=%d; b=%d\n", a, b);
    }
    printf("Values in main, a=%d; b=%d\n", a, b);
    a=0;
    b=3;
    if(a++ && --b){
        printf("Values inside AND If, a=%d; b=%d\n", a, b);
    }
    printf("Values at last, a=%d; b=%d\n", a, b);
    return 0;
}
