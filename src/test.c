int f(){
    return 0;
}

struct point{
    int x;
}
int main()
{
    int * x , y ;
    x = &y ;
    x  = x * y; // should not give error
    return 0 ;
}