int main()
{
    int r = 3, c = 4, i, j, count;
  
    int *arr[3];
    for (i=0; i<r; i++)
         arr[i] = (int *)malloc(c * sizeof(int));
  
    
    count = 0;
    for (i = 0; i <  r; i++)
      for (j = 0; j < c; j++)
         arr[i][j] = ++count; 
  
    for (i = 0; i <  r; i++)
      for (j = 0; j < c; j++)
         printf("%d ", arr[i][j]);
  
   return 0;
}