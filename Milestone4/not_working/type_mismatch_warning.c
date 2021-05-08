int post(int* a)
{
    return (*a)++ ;
}
int main()
{
    int a = 5 ;
    printf("post = %d", post(&a)) ;
    return 0 ;
}