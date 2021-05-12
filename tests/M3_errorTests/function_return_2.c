void x(int y)
{
    return 5; // wrong error, not a major issue
}

int main()
{
    int x ;
    x(x) ;
}