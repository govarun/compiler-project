void change(char *b)
{
    *b = 'L' ;
    return ;
}
void not_change(char b)
{
    printf("%c\n", b) ;
    b = 'A' ;
    return ;
}
void print(char b)
{
    printf("%c\n", b) ;
    return ;
}
int main()
{
    char a = 'S' ;
    not_change(a) ;
    print(a) ;
    change(&a) ;
    print(a) ;
    return 0;
}