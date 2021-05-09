// #include<stdio.h>
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
