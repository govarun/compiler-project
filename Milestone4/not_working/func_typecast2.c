int int_return(int a , float b)
{
    return a*b ;
}

float float_return(int a , float b)
{
    return a*b ;
}

int main()
{
    int a = 5 ;
    float b = 2.5 ;
    int ans[2][4] ;
    float ans2[2][4] ;

    int i , j ;

    ans[0][0] = int_return(a , a) ;
    ans[0][1] = int_return(a , b) ;
    ans[0][2] = int_return(b , a) ;
    ans[0][3] = int_return(b , b) ;

    ans2[0][0] = int_return(a , a) ;
    ans2[0][1] = int_return(a , b) ;
    ans2[0][2] = int_return(b , a) ;
    ans2[0][3] = int_return(b , b) ;

    ans[1][0] = float_return(a , a) ;
    ans[1][1] = float_return(a , b) ;
    ans[1][2] = float_return(b , a) ;
    ans[1][3] = float_return(b , b) ;

    ans2[1][0] = float_return(a , a) ;
    ans2[1][1] = float_return(a , b) ;
    ans2[1][2] = float_return(b , a) ;
    ans2[1][3] = float_return(b , b) ;

    for(i = 0 ; i < 2 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            printf("i = %d, j = %d, ans[i][j] = %d\n", i , j , ans[i][j]) ;
        }
        printf("\n") ;
    }
    for(i = 0 ; i < 2 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            printf("i = %d, j = %d, ans2[i][j] = %d\n", i , j , ans2[i][j]) ;
        }
        printf("\n") ;
    }
    return 0 ;
}