int main()
{
    int n = 6 ;
    int arr[6] ;
    int i ;
    for(i = 0 ; i < 6 ; i++)
    {
        arr[i] = i+1 ;
        printf("i = %d, arr[i] = %d\n", i , *(arr + i)) ;
    }
    return 0 ;
}