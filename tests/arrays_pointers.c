typedef struct point{
    int x ;
    int y ;
}   ;

int main()
{
    point p[5] ;
    int arr[10] ;
    for(int i = 0 ; i < 10 ; i++)
    {
        arr[i] = i ;
    }
    for(int i = 0 ; i < 5 ; i+=2)
    {
        p[i].x = arr[2*i] ;
        p[i].y = arr[2*i + 1] ;
    }

    point *q = &p, *r = &p[0] , *s = &p[1] ;
    int *x = &(arr + 2) ; 
    *x = 5 ;
    int **z = &(x) ; //check handling of double pointers
    *(*z) = 10 ;
    return ;
}