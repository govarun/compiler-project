struct point{
    int x ;
    long int y , z ;
    //return 5 ; // giving error
} // no error even on missing semicolon
int main()
{
    struct point a ;
    //point b ; // This is giving syntax error
    return 1 ;
}