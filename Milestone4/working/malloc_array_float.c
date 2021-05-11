float eps = 0.05 ;
float lim = 0.04 ;
int main()
{
    float* arr = (float*)malloc(50 * sizeof(float)) ;
    int i ;
    for(i = 0 ; i < 50 ; i++)
    {
        *(arr + i) = i ;
    }
    for(i = 0 ; i < 50 ; i++)
    {
        printf("i = %d, arr[i] = %f\n", i , *(arr + i)) ;
    }
    
    return 0 ;
}
