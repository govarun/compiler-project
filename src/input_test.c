int fact(int n){
    if(n == 0)  return 1;
    else return n*fact(n-1);
}
int main(){
    int n;
    printf("Enter number to calculate factorial : ");
    scanf("%d", &n);
    printf("The factorial is %d\n", fact(n));
    return 0;
}