const int n = 100 ;
int main()
{
    int x = n ;
    x++ ;
    x-- ;

    x = x+5 ;
    x = x-5 ;
    x = x*5 ;
    x = x/5 ;
    x = x%51 ;

    if(((x|n == 100) || (x&n != 100)) && ((x^1)%2 == 0))
    {
        int y = 0 ;
        int z = 1 ;
        if((~y) && ((z << 1) == 2) && (((z << 2)>>1) != 3*z))
        {
            int a = 5 ;
        }
    }
    x = 50 ;
    int y = 40 ;
    int z = 60 ;
    int xd = 50 , yd = 40 ;

    if(z > x && z >= x && y < x && y <= x && xd == x && yd != xd)
    {
        ;
    }
    return 0 ;
}