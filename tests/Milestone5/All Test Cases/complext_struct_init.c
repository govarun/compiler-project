struct point{
    int x , y ;
};
struct rectangle{
    struct point p[4] ;
};
void print(struct rectangle r)
{
    printf("(%d , %d) (%d , %d) (%d , %d) (%d , %d)\n", r.p[0].x , r.p[0].y, r.p[1].x , r.p[1].y , r.p[2].x , r.p[2].y , r.p[3].x , r.p[3].y) ;
    return ;
}
int main()
{
    struct rectangle r = {{{1,1} , {2 , 2} , {3 , 3} , {4 , 4}}} ;
    print(r) ;
    return 0 ;
}