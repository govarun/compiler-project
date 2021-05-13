int calc_odd(int) ;
int calc_even(int) ;

int main()
{
    printf("val = %d\n", calc_even(4)) ;
    printf("val = %d\n", calc_odd(4)) ;
    printf("val = %d\n", calc_even(5)) ;
    printf("val = %d\n", calc_odd(5)) ;
    return 0 ;
}

int calc_odd(int n)
{
    if(n%2 == 0)
        return -1 ;
    return 2*n + calc_even(n-1);
}
int calc_even(int n)
{
    if(n%2)
        return -1 ;
    if(n == 0)
        return 0 ;
    return n/2 + calc_odd(n-1) ;

}