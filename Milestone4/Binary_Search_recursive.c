void binary_search(int arr[] , int l , int r , int val)
{
    int mid ;
    if(l > r)
    {
        printf("not present\n") ;
        return ;
    }
    mid = (l+r)/2 ;
    if(arr[mid] == val)
    {
        printf("ans = %d\n", mid) ;
        return ;
    }
    if(arr[mid] > val)
        return binary_search(arr , l , mid-1 , val) ;
    return binary_search(arr , mid+1 , r , val) ;
}
int main()
{
    int arr[500] ;
    int i = 0 ; 
    for(i = 0 ; i < 500 ; i++)
        arr[i] = i+1 ;
    binary_search(arr , 0 , 499 , 147) ;
    binary_search(arr , 0 , 499 , 700) ;
    binary_search(arr , 0 , 499 , 0) ;
    return 0 ;
}