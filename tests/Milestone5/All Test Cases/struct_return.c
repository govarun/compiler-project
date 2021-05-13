struct point{
    float x , y ;
} ;

struct point make_point(float x , float y)
{
    struct point p;
    (p.x) = x ;
    (p.y) = y ;
    return p ;
}
int main()
{
    float x = 1 , y = 2 ;
    struct point p = make_point(x , y) ;
    printf("(%f , %f)\n", p.x , p.y) ;
    return 0 ;
}