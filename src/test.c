struct point{
    int x ;
    int y ;
    int z[5] ;
}

struct list{
    struct point p[10] ;
}
int main()
{
    struct point p ;
    struct list l ;
    p.z[5] = 4 ;
    l.p[5][2].z[4] = 3 ;
    
}