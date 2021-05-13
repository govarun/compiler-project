typedef struct point{
    float x , y ;
} point;

point upper_right = {2 , 2} ;

point get_vector(point p1 , point p2) // returns vector from p1 to p2
{
    point p ;
    p.x = p2.x - p1.x ;
    p.y = p2.y - p1.y ;
    return p;
}

int dist_(point p1 , point p2) // return distance beyween two points
{
    float x = p1.x - p2.x ;
    float y = p1.y - p2.y ;
    return (x*x + y*y) ;
}

float cross(point p1 , point p2) // return cross product of two vectors
{
    return (p1.x*p2.y - p2.x*p1.y) ;
}

int main()
{
    point x = {2 , 1} ;
    point y = {1 , 2} ;

    point v = get_vector(x , y) ;
    int dist = dist_(x , y) ;
    float c = cross(x , y) ;

    printf("v.x = %f, v.y = %f, dist = %d, cross = %f\n", v.x , v.y , dist , c) ;
    return 0 ;
}
/*
v.x = -1.000000, v.y = 1.000000, dist = 2, cross = 3.000000
*/