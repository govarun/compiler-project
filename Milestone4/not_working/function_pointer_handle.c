int post(int* a)
{
    return (*a)++ ;
}
int main()
{
    int a = 5 ;
    printf("post = %d\n", post(&a)) ;
    printf("new_value of a = %d\n", a) ;
    return 0 ;
}