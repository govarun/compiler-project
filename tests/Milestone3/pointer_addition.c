int main()
{
    int *x , y ;
    x = &y ;
    x  = x + 1; // should not give error
    return 0 ;
}