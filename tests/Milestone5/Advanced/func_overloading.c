void get_type(int a)
{
    printf("I am an int\n") ;
    return ;
}
void get_type(float a)
{
    printf("I am a float\n") ;
    return ;
}

void get_type(int a , int b)
{
    printf("I am int and int\n") ;
    return ;
}
void get_type(int a , float b)
{
    printf("I am int and float\n") ;
    return ;
}

void get_type(float a , int b)
{
    printf("I am float and int\n") ;
    return ;
}

void get_type(float a , float b)
{
    printf("I am float and float\n") ;
    return ;
}

void get_type(int a , int b , int c)
{
    printf("I have 3 args\n") ;
    return ;
}
int main()
{
    int a = 5 ;
    float b = 2 ;

    get_type(a) ;
    get_type(b) ;

    printf("\n") ;

    get_type(a , a) ;
    get_type(a , b) ;
    get_type(b , a) ;
    get_type(b , b) ;

    printf("\n") ;

    get_type(a , a , a) ;
    get_type(a , b , a) ;
    get_type(b , a , a) ;
    get_type(a , a , b) ;
    get_type(b , b , b) ;

    return 0 ;
}