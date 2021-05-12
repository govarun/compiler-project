float eps = 0.05 ;
float lim = 0.04 ;
int main()
{
    float a , b , c , d ;
    float *e , *f ;
    a = 1.1 , b = 2.2 , c = 3.3 , d = 4.4 ;
    e = &b;
    f = e+1 ;

    printf("e_val = %f , f_val = %f\n", *e , *f) ;
    return 0 ;
}
