int main()
{
    {
        int a = 1e5 , b = 1e-5 ;
        float c = 1e5 , d = 1e-5 , e = -1e5 , f = -1e-5 ;
        float g = -1.2e-5 , h = -1.2e5 , i = -1.2e+5 ;
    }
    {
        int a = 1E5 , b = 1E-5 ;
        float c = 1E5 , d = 1E-5 , e = -1E5 , f = -1E-5 ;
        float g = -1.2E-5 , h = -1.2E5 , i = -1.2E+5 ;
    }
    {
        float a = 0x5e2 ; 
        float b = 0x5ea ;
    }
    {
        float a = 1.2e5.0 , b = 1.2e5.1 ; 
    }
    {
        long long a = (1LL) ;
        long long b = (1ll) ;
        long long c = (LL1) ; 
        long long d = (1LL << 50) ;
    }
    return 0 ;
}