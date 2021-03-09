int main(){
    int x = 0, i = 0;
    for(i=0;i<5;++i){
        int y=0;
        x += i;
    }
    /*
    for(int j=0;j<5;++j){
        x += j;
    }
    // This will result in error. Declaration in start condition of for loop not allowed.
    */
    return 0;
}
