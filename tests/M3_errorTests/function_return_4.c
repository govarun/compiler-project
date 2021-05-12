int *f(int x)
{
    return f(x-1) ;
}
int main()
{
    int x ;
    f(x) ;
    return 0 ;
}