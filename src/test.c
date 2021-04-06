struct point
{
    int p1, p2;
    int a[10];
} 
int main()
{
    struct line
    {
        struct point p1;
        struct point p2;
    } 
    struct line l1;
    l1.p1.p1;
}