float eps = 1e-4 ;
void get_val(float* val, int a , float b)
{
    printf("b = %f\n", b) ;
    (*val) = (a + b) ;
    return ;
}

int main()
{
    int a = 1 , b = -10 ;
    float val ;
    get_val(&val , a , b) ;
    printf("val = %f", val) ;
    return 0 ;
}
