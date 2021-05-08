int calc_odd(int) ;
int calc_even(int) ;

int val[10] ;

int main()
{
    
    int i = 0 ;
    for(i = 0 ; i < 10 ; i++)
    {
        val[i] = -1 ;
    }
    calc_odd(9) ;
    printf("\n") ;
    for(i = 0 ; i < 10 ; i++)
    {
        printf("i = %d, val = %d\n", i , val[i]) ;
    }
    printf("\n") ;
    calc_even(8) ;
    return 0 ;
}

int calc_odd(int n)
{
    printf("n = %d\n", n) ;
    if(n%2 == 0)
        return -1 ;
    if(val[n] != -1)
        return val[n] ;
    return val[n] = 2*n + calc_even(n-1);
    
}
int calc_even(int n)
{
    printf("n = %d\n", n) ;
    if(n%2)
        return -1 ;
    if(n == 0)
        return val[n] = 0 ;
    if(val[n] != -1)
        return val[n] ;
    return val[n] = n/2 + calc_odd(n-1);
    
}

