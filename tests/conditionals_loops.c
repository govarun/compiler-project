char a = 'c' ;
char b = c ; // should throw error in later stages
const int n = 100 ;
static double d = 50 ;
unsigned int m = 500 ;
extern int c ;

int main()
{
    printf("%d \n", n) ;
    for(; n > 0 ; n--)
    {
        if(n > 50)
            continue ;
        else
        {
            if(n < 10)
                break ;
            else
            {
                auto x = d ;
                auto y = sizeof(d) ;
            }
        }
    }
    while(n > 0)
    {
        n-- ;
    }
    return 0;
}