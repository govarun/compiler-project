int ackermann_recursion(int m , int n)
{
    if(m == 0)
        return n+1 ;
    
    if(n == 0)
    {
        return ackermann_recursion(m-1 , 1) ;
    }

    return ackermann_recursion(m-1 , ackermann_recursion(m , n-1)) ;
}
int main()
{   
    int i , j ;
    for(i = 0 ; i < 4 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
            printf("i = %d, j = %d, val = %d\n", i , j , ackermann_recursion(i , j)) ;
        printf("\n") ;
    }
    return 0 ;
}