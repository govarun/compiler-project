#include <stdio.h>

void f(int *x, double y)
{
    return;
}

int main()
{
    int *x;
    (x += 2);
    return 0;
}