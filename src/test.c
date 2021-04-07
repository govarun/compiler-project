<<<<<<< HEAD
=======
int **f(int x)
{
    int * y;
    return y ;
}
>>>>>>> 9242018f5d338d8073e55c456ac3e3040e1cf1a4
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