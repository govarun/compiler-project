int min(int a , int b)
{
    if(a < b)
        return a ;
    return b ;
}

int min(int a , int b , int c)
{
    return min(a , min(b , c)) ;
}

void print(int a)
{
    printf("I am a int : %d\n", a) ;
    return ;
}

void print(float b)
{
    printf("I am a float : %f", b) ;
    return ;
}

int main()
{
    int a = 5 , b = 2 , c = 7 ;
    float d = 5.5 ;


    printf("%d\n", min(a , b , c)) ;
    print(a) ;
    print(d) ;
    return 0 ;
}