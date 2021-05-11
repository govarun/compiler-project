float eps = 0.05 ;
float lim = 0.04 ;

void change_val(float *f)
{
    (*f) *= 2 ;
    return  ;
}

float not_change_val(float f)
{
    f *= 2 ;
    return f ;
}

int main()
{
    float a = 1.2 , b;
    change_val(&a) ;
    printf("new_val of a = %f\n", a) ;
    b = not_change_val(a) ;
    printf("a = %f , b = %f\n", a , b) ;
    return 0 ;
}
/*
new_val of a = 2.400000
a = 2.400000 , b = 4.800000
*/