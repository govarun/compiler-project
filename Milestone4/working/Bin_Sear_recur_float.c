int iter = 30 ;
void binary_search(int cnt , float l , float r)
{
    float mid = (l+r)/2 ;
    float val = 5*mid + 2 ;
    if(cnt >= iter)
        return ;
    
    printf("mid = %f, val = %f\n", mid , val) ;
    if(val > 0)
        return binary_search(cnt+1 , l , mid) ;
    else
        return binary_search(cnt+1 , mid , r) ;
}
int main()
{   float l = -1000 , r = 1000 ;
    binary_search(0 , l , r) ;
    return 0 ;
}