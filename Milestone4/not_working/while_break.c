int main()
{
    int arr[500] ;
    int i = 0 ;
    while(i < 500)
    {
        arr[i] = i+1 ;
        i++ ;
        if(i == 150)
        {
            break ; // continue also not working
        }
    }
    return 0 ;
}