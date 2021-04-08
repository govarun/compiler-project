union point{
    int x;
    char c;
    long a[2];
}

int main(){
    union point p;
    p.x = 4;
    return 0;
}