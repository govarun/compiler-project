struct point
{
    int x;
    int y;
}

struct line{
    struct point *p1, p2;
    int x, *y;
}

int main()
{
    struct line *l;
    // l->p1;
    l->p1->x = 5;
    l->p1.x = 3;
    // int x, y, *z;
    return 0;
}