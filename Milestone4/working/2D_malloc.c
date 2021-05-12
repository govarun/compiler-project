int main(){
    int** arr;
    int i = 0, j = 0;
    arr = (int**)malloc(4*sizeof(int*));
    for(i = 0; i < 4; i++){
        arr[i] = (int*)malloc((i+1)*sizeof(int));
    }
    return 0;
}