int main()
{
    int z ;
    int x = 5 ;
    {
        z = x ; // giving traceback error
    }
    int z = x ;
    return 0 ;
}