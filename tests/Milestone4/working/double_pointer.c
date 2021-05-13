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
    change(&x , &z) ;
    printf("%d\n", z);
    return 0 ;
}