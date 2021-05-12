int main(){
    int** arr;
    int i = 0, j = 0;
    arr = (int**)malloc(4*sizeof(int*));
    for(i = 0; i < 4; i++){
        arr[i] = (int*)malloc((i+1)*sizeof(int));
    }
    for(i = 0; i < 4; i++){
        for(j = 0; j <= i; j++){
            arr[i][j] = i+j;
        }
    }
    for(i = 0; i < 4; i++){
        for(j = 0; j <= i; j++){
            printf("[%d %d] ", *(*(arr + i) + j), arr[i][j]);
        }
        printf("\n");
    }
    return 0;
}