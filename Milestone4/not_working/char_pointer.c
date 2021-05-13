void print(char c)
{
    printf("%c", c) ;
}
int main () {

   char greeting[6] = {'H', 'e', 'l', '\0', 'o', '\0'};
   char *s = greeting ;
   printf("%s\n", s);
   return 0;
}