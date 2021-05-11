struct point{
    float x , y ;
} ;


int dist(struct point p1 , struct point p2)
{
    return (p2.x - p1.x + p2.y - p1.y) ;
}

int main()
{
    struct point x = {2 , 1} ;
    struct point y = {4 , 2} ;
    int d = dist(x , y) ;
    printf("dist = %d", d) ;
    return 0 ;
}
/* dist = 3 */