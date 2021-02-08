int main()
{
    int a = 052 , b = 072 , c = -052 ;
    int d = - 052 ;
    int e = 082 , f = 092 , g = 028 , h = 029 ; // invalid
    int i = 05a5 ; // invalid

    int j = 0b0110 , k = 0b1100 ;
    int l = 0b0201 ; // invalid

    int m = 0x05 , n = 0x50 ;
    int p = 0x5a2 , q = 0x5f2 , r = 0x5g2 ; // r is invalid

    int s = 0Xab , t = 0XAB , u = 0XAG , v = 0xAB ; // valid

    int w = 0c0 ; // invalid 
    return ;

}