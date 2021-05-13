struct point{
    int x, y;
    int z[5];
    char c;
};

struct point p = {2, 3, {2,4,8,16}, 'c'};

int main(){
    int i =0;
    printf("%d %d\n", p.x, p.y);
    for(i = 0; i<5; i++)    printf("%d ", p.z[i]);
    printf("\n%c\n", p.c);
    return 0;
}