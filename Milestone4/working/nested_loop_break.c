int main()
{
    int x = 4 , y = 5 ;
    while(x > 0)
    {
        y = 5 ;
        while(y > 0)
        {
            if(x == 2 && y == 3)
                break ;
            printf("x = %d, y = %d\n", x , y) ;
            y-- ;
        }
        x-- ;
    }
    return 0;
}