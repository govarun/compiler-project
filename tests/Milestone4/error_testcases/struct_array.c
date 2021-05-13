struct point{
    int x ; 
    float y ;
};
int main()
{
    struct point arr[10] ;
    int i ;
    for(i = 0 ; i < 10 ; i++)
    {
        arr[i].x = i+1 ;
        arr[i].y = (i+1)*2.1 ;
    }
    for(i = 0 ; i < 10 ; i++)
    {
        printf("(%d, %f) ", arr[i].x , arr[i].y) ;
    }
    return 0 ;
}