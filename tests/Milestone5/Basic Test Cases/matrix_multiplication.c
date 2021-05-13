int main()
{
    int a[3][5] , b[5][4] , c[3][4] ;
    int i , j , k ;
    for(i = 0 ; i < 3 ; i++)
    {
        for(j = 0 ; j < 5 ; j++)
        {
            a[i][j] = i+j+1 ;
        }
    }
    for(i = 0 ; i < 5 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            b[i][j] = i+j+1 ;
        }
    }
    for(i = 0 ; i < 3 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            c[i][j] = i+j+1 ;
        }
    }
    for(i = 0 ; i < 3 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            for(k = 0 ; k < 5 ; k++)
            {
                c[i][j] += a[i][k]*b[k][j] ;
                // replacing this with c[i][j] = c[i][j] + a[i][k]*b[k][j] is working ..
            }
        }
    }

    for(i = 0 ; i < 3 ; i++)
    {
        for(j = 0 ; j < 5 ; j++)
        {
            printf("%d ", a[i][j]) ;
        }
        printf("\n") ;
    }

    printf("\n") ;

    for(i = 0 ; i < 5 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            printf("%d ", b[i][j]) ;
        }
        printf("\n") ;
    }

    printf("\n") ;
    for(i = 0 ; i < 3 ; i++)
    {
        for(j = 0 ; j < 4 ; j++)
        {
            printf("%d ", c[i][j]) ;
        }
        printf("\n") ;
    }
    return 0 ;
}

/*
1 2 3 4 5 
2 3 4 5 6 
3 4 5 6 7 

1 2 3 4 
2 3 4 5 
3 4 5 6 
4 5 6 7 
5 6 7 8 

56 72 88 104 
72 93 114 135 
88 114 140 166
*/