int main()
{
    int * x , y ;
    x = &y ;
    x  = x * y; // should not give error
    return 0 ;
}