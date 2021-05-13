struct point{
    int x ; 
    float y ;
};
int main()
{
    struct point arr[2][2] ;
    int i , j;
    for(i = 0 ; i < 2 ; i++)
    {
        for(j = 0 ; j < 2 ; j++)
        {
            arr[i][j].x = i+j ;
            arr[i][j].y = (i+j)*2.1 ;
        }
    }
    for(i = 0 ; i < 2 ; i++)
    {
        for(j = 0 ; j < 2 ; j++)
            printf("(%d, %f) ", arr[i][j].x , arr[i][j].y) ;
        printf("\n") ;
    }
    return 0 ;
}