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
    calc_odd(9 , val) ;
    printf("\n") ;
    for(i = 0 ; i < 10 ; i++)
    {
        printf("i = %d, val = %d\n", i , val[i]) ;
    }
    printf("\n") ;
    calc_even(8 , val) ;
    return 0 ;
}

int calc_odd(int n , int val[])
{
    printf("n = %d\n", n) ;
    if(n%2 == 0)
        return -1 ;
    if(val[n] != -1)
        return val[n] ;
    val[n] = 2*n + calc_even(n-1 , val);
    printf("val of %d = %d\n", n , val[n]) ;
    return val[n];
}
int calc_even(int n , int val[])
{
    printf("n = %d\n", n) ;
    if(n%2)
        return -1 ;
    if(n == 0)
        return val[n] = 0 ;
    if(val[n] != -1)
        return val[n] ;
    val[n] = n/2 + calc_odd(n-1 , val);
    printf("val of %d = %d\n", n , val[n]) ;
    return val[n];
}
/*
n = 9
n = 8
n = 7
n = 6
n = 5
n = 4
n = 3
n = 2
n = 1
n = 0
val of 1 = 2
val of 2 = 3
val of 3 = 9
val of 4 = 11
val of 5 = 21
val of 6 = 24
val of 7 = 38
val of 8 = 42
val of 9 = 60

i = 0, val = 0
i = 1, val = 2
i = 2, val = 3
i = 3, val = 9
i = 4, val = 11
i = 5, val = 21
i = 6, val = 24
i = 7, val = 38
i = 8, val = 42
i = 9, val = 60

n = 8
*/
