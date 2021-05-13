void print(char c)
{
    printf("%c", c) ;
}
int main () {

   char greeting[6] = {'H', 'e', '\0', 'l', 'o', '\0'};
   int i = 0 ;
   printf("%s\n", greeting);
   return 0;
}