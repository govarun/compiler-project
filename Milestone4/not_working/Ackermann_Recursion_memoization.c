
int val[100][100] ;
int ackermann_recursion(int m , int n)
{
    printf("m = %d, n = %d\n", m , n) ;
    if(val[m][n] != -1)
        return val[m][n] ;
    if(m == 0)
        return n+1 ;
    
    if(n == 0)
    {
        return val[m][n] = ackermann_recursion(m-1 , 1) ;
    }

    return val[m][n] = ackermann_recursion(m-1 , ackermann_recursion(m , n-1)) ;
}
int main()
{
    int i , j ;
    for(i = 0 ; i < 100 ; i++)
        for(j = 0 ; j < 100 ; j++)
            val[i][j] = -1 ;
    
    for(i = 0 ; i < 4 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
            //printf("i = %d, j = %d, val = %d\n", i , j , ackermann_recursion(i , j)) ;
        printf("\n") ;
    }
    return 0 ;
}