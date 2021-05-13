int fib(int n){
    if(n == 0 || n == 1)  return n;
    return fib(n-1) + fib(n-2);
}
int main(){
    int n = 20;
    int arr[20] = {0, 1};
    int i = 0;
    for(i = 2; i < 20; i++){
        arr[i] = arr[i-1] + arr[i-2];
    }
    for(i = 0; i < 20; i++){
        printf("%d ", arr[i]);
    }
    printf("\n");
    for(i = 0;i < 20; i++){
        printf("%d ", fib(i));
    }
    printf("\n");
    return 0;
}