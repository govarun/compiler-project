int sum_return(int a , int b)
{
    return a + b ;
}
int shift_return(int a , int b)
{
    return (a << b) ;
}

int assign_return(int a , int b)
{
    return a = b ;
}

int comp_return(int a , int b)
{
    return (a < b) ;
}

int eq_return(int a , int b)
{
    return (a == b) ;
}
int multi_return(int a, int b)
{
    return sum_return(a , b) + shift_return(a , b) + comp_return(a , b) ;
}

int tern_return(int a , int b) // giving error
{
    return (eq_return(a , b) ? sum_return(a , b) : shift_return(a , b)) ;
}

int main()
{
    int a = 4 , b ;
    b = 5 ;
    // printf("sum = %d, shift = %d , assign = %d\n",sum_return(a, b) , shift_return(a , b) , assign_return(a , b)) ;
    // printf("comp = %d, eq = %d\n", comp_return(a , b) , eq_return(a, b)) ;
    // printf("multi = %d\n", multi_return(a , b) ) ;
    printf("tern = %d\n", tern_return(a , b)) ;
    return 0 ;

}
