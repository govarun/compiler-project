
int main()
{
    int arr[500] ;
    int i = 0 ;
    int l = 0 , r = 499 , ans , mid ;
    for(; i < 500 ; i++)
    {
        arr[i] = i+1 ;
    }
    while(l <= r)
    {
        mid = (l+r)/2 ;
        printf("mid = %d\n", mid) ;
        if(arr[mid] == 150)
        {
            ans = mid ;
            break ;
        }
        if(arr[mid] > 150)
            r = mid-1 ;
        else
            l = mid+1 ;
    }
    printf("ans = %d", ans) ;
    return 0 ;
}