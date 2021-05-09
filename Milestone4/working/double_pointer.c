void change(int **x , int* y)
{
    *x = y ;
    return ;
}
int main()
{
    int y = 4 ;
    int* x = &y ;
    int z = 0 ;
    printf("before change : x = %d\n", x) ;
    
    change(&x , &z) ;
    printf("after change : x = %d\n", x) ;
    printf("addr of y = %d, z = %d\n", &y , &z) ;
    return 0 ;
}