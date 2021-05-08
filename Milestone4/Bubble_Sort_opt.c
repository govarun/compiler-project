void swap(int *a , int *b)
{
    int c = *a ;
    *a = *b ;
    *b = c ;
    return ;
}

void print_arr(int arr[] , int left , int right)
{
    int i = left ;
    for(; i <= right ; i++)
    {
        printf("%d ", arr[i]) ;
    }
    printf("\n") ;
    return ;
}

void bubblesort(int arr[] , int n)
{
    int i = 0 , j = 0 ;
    for(i = 0 ; i < n ; i++)
    {
        int flag = 0 ;
        for(j = 0 ; j < n-1 ; j++)
        {
            if(arr[j] > arr[j+1])
            {
                swap(&arr[j] , &arr[j+1]) ;
                flag = 1 ;
            }
        }
        printf("i = %d : ", i) ;
        print_arr(arr , 0 , 5) ; 
        if(flag == 0)
        {
            printf("No change : Terminating ...\n") ;
            return ;
        }
    }
    return ;
}   

int main()
{
    int i , j , n = 6 ;
    int arr[6] ;
    arr[0] = 0 , arr[1] = 5 , arr[2] = 2 , arr[3] = 1 , arr[4] = 4 , arr[5] = 5 ;
    printf("Before Bubble_sort : ") ;
    print_arr(arr , 0 , 5) ;
    bubblesort(arr , 6) ;
    printf("After Bubble_sort : ") ;
    print_arr(arr , 0 , 5) ;
    return 0 ;
}