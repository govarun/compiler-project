int main()
{
    int arr[500] ;
    int i = 0 ;
    while(i < 50)
    {
        arr[i] = i+1 ;
        i++ ;
        if(i == 15)
        {
            continue ;
        }
        printf("i = %d\n", i) ;
    }
    return 0 ;
}