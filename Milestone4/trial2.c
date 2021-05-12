int int_return(int a , float b)
{
    
    return a*b ;
}
int main()
{
    int a = 5 ;
    float b = 5 ;
    int arr[1][1] ;
    arr[0][0] = int_return(a , b) ;
    printf("val = %d\n", arr[0][0]) ;
    return 0 ;
}