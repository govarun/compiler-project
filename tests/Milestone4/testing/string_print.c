int main () {

    char *s = "Lavish" ;
    int i = 0;
    while(s[i] != NULL)
    {
        printf("%c", s[i]) ;
        i++ ;
        if(i > 6)
            break ;
    }
    return 0 ;
}