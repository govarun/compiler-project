int main()
{
    int a, *p, **ptr, ***pt, ****ps, z;
    a=4;
    p = &a;
    ptr = &p;
    pt = &ptr;
    ps = &pt;

    printf("%d\n", ****ps);

    a = 8;

    printf("%d\n", ****ps);
    return 0;
}