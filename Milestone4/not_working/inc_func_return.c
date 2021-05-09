// giving wrong values .. first look at function_pointer_handle .. that is a simpler version

int post(int* a)
{
    return (*a)++ ;
}
int pre(int* a)
{
    return ++(*a) ;
}
int pre_pre(int* a , int* b)
{
    return ++(*a) * ++(*b) ;
}
int pre_post(int* a , int* b)
{
    return ++(*a) * (*b)++ ;
}
int post_pre(int* a , int* b)
{
    return (*a)++ * ++(*b) ;
}
int post_post(int* a , int* b)
{
    return (*a)++ * (*b)++ ;
}

int main()
{
    int a = 2 , b = 3 ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("pre : %d\n", pre(&a)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("post : %d\n", post(&a)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("pre_pre : %d\n", pre_pre(&a , &b)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("pre_post : %d\n", pre_post(&a , &b)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("post_pre : %d\n", post_pre(&a , &b)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    printf("before : a = %d , b = %d\n", a , b) ;
    printf("post_post : %d\n", post_post(&a , &b)) ;
    printf("after : a = %d , b = %d\n\n", a , b) ;

    return 0 ;

} 
/*
before : a = 2 , b = 3
pre : 3
after : a = 3 , b = 3

before : a = 3 , b = 3
post : 3
after : a = 4 , b = 3

before : a = 4 , b = 3
pre_pre : 20
after : a = 5 , b = 4

before : a = 5 , b = 4
pre_post : 24
after : a = 6 , b = 5

before : a = 6 , b = 5
post_pre : 36
after : a = 7 , b = 6

before : a = 7 , b = 6
post_post : 42
after : a = 8 , b = 7
*/