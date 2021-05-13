
int main()
{
    int a = 5 , b = 2 , i = 0;
    float l = -1000 , r = 1000 , mid;
    for(i = 0 ; i < 100 ; i++)
    {
        mid = (l+r)/2 ;
        if((a*mid + b) > 0)
            r = mid ;
        else
            l = mid ;
        
    }   
    printf("root = %f", l) ;
    return 0 ;
}