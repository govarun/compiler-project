int f(int x , char y)
{
    {
        x = y ;
    }
    return 0 ;
}
int main()
{
    f(x , y) ; // giving traceback error
    return 0 ;
}