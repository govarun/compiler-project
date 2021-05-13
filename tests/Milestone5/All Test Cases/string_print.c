int main () {

    char *s = "Lavish" ;
    int i = 0;
    while(s[i] != '\0')
    {
        printf("%c", s[i]) ;
        i++ ;
        if(i > 6)
            break ;
    }
    return 0 ;
}