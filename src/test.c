static int x = 5 ;

int main()
{
    int z = 5;
    int x = 5 ;
    {
        int x = 4 ;
        int z = 2 ;
        z = x ;
    }
    x = z ;
    
}
