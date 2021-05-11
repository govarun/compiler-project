// wrong value of g .. commenting out aa to f results in correct value of g
float eps = 0.05 ;
float lim = 0.0001 ;
int main()
{
    float x = 1.0 , y = 1.9 , z = 0.9 , a = 0.8 ;

    int aa = x < y ;
    int b = x > y ;
    int c = (x == y) ;
    int d = (x+z == y) ;
    int e = (x+a < y) ;
    int f = (x+a > y) ;
    int g = (y-x < z) ;
    /*int h = (y-x == z) ;
    int i = (y-x > z) ;*/
    printf("%d %d %d %d %d %d %d %d %d\n",aa,b,c,d,e,f,g,h,i) ;
    return 0 ;
}
//1 0 0 1 1 0 0 1 0