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
    p.z[5] = 4 ;
    struct list l ;
    l.p[5].z[4] = 3 ;
    
}