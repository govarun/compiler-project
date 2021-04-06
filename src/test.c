struct point{
    int x;
    char y ;
}

struct line{
    struct point p ;
    int y ;
}

int main()
{
    struct line l;
    l.p.x;
    return 0;
}