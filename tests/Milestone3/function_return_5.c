int* f(int a)
{
    int *b = &a ;
    return b ; // should not throw an error
}
int main()
{
    int x = 5 ;
    return 0 ;
}