int main()
{
    int *x , y ;
    x = &y ;
    x *= 5 ; // currently giving warning, should throw an error, not a major issue?
    return 0 ;
}