int f(int a)
{
    int *b = &a ;
    return b ;
}
int main()
{
    int x = 5 ;
    int y = *f(x) ; // should throw an error
    return 0 ;
}