int main()
{
    const char *a = "Lavish Gupta" ;
    char *b = (char*)malloc(14*sizeof(char)) ;
    strcpy(b , a) ;
    printf("len = %d", strlen(b)) ;
    return 0 ;
}