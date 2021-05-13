struct point{
    float x , y ;
} ;


struct point get_vector(struct point p1 ,struct point p2) // returns vector from p1 to p2
{
    struct point p ;
    p.x = p2.x - p1.x ;
    p.y = p2.y - p1.y ;
    return p;
}


int main()
{
    struct point x = {2 , 1} ;
    struct point y = {1 , 2} ;
    struct point p = get_vector(x , y) ;
    printf("p.x = %f, p.y = %f\n", p.x , p.y) ;
    return 0 ;
}
