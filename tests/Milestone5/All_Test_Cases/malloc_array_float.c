float eps = 0.05 ;
float lim = 0.04 ;
int main()
{
    float* arr = (float*)malloc(20 * sizeof(float)) ;
    int i ;
    for(i = 0 ; i < 20 ; i++)
    {
        if(i%2 == 0)
            arr[i] = i ;
        else
        {
            (*(arr + i)) = (*(arr + i - 1))+1 ;
        }
    }
    for(i = 0 ; i < 20 ; i++)
    {
        printf("i = %d, arr[i] = %f\n", i , *(arr + i)) ;
    }
    
    return 0 ;
}
