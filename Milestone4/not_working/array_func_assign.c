int calc_odd(int , int[]) ;
int calc_even(int , int[]) ;

int main()
{
    int val[10] ;
    int i = 0 ;
    for(i = 0 ; i < 10 ; i++)
    {
        val[i] = -1 ;
    }
    printf("val of 0 = %d\n", calc_even(0 , val)) ;
    return 0 ;
}

int calc_odd(int n , int val[])
{
    val[n] = 2*n + calc_even(n-1 , val);
    return val[n];
}
int calc_even(int n , int val[])
{
    
    if(n == 0)
        return val[n] = 0 ;
    
    val[n] = n/2 + calc_odd(n-1 , val);
    return val[n];
}

