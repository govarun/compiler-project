void swap(int *a, int *b){
    int tmp;
    tmp = *a;
    *a = *b;
    *b = tmp;
    return;
}
int main(){
    int a = 3, b = 5;
    printf("%d , %d\n", a, b);
    swap(&a, &b);
    printf("%d , %d\n", a, b);
    return 0;
}