struct point{
    float x, y;
};
struct line{
    float a, b, c;
};

struct line getLine(struct point p1, struct point p2){
    struct line l;
    l.a = p1.y - p2.y;
    l.b = p2.x - p1.x;
    l.c = p2.x * p1.y - p1.x * p2.y;
    return l;
}

struct point getIntersection(struct line l1, struct line l2){
    struct point p = {0, 0};
    if(l1.a != 0 && l2.a != 0 && l1.b/l1.a == l2.b/l2.a){
        printf("Lines are parallel, returning origin\n");
    }
    if(l1.b != 0 && l2.b != 0 && l1.a/l1.b == l2.a/l2.b){
        printf("Lines are parallel, returning origin\n");
    }
    p.x = (l1.c * l2.b - l2.c *l1.b)/(l1.a * l2.b - l2.a * l1.b);
    p.y = (l1.c * l2.a - l2.c * l1.a)/(l1.b * l2.a - l2.b * l1.a);
    return p;
}

int main(){
    struct point p1 = {1, 1}, p2 = {1, 3}, p3 = {5, -2}, p4 = {0, 3.5}, p;
    struct line l1 = getLine(p1, p2);
    struct line l2 = getLine(p3, p4);
    p = getIntersection(l1,  l2);
    printf("line1 : %fx + %fy = %f\n", l1.a, l1.b, l1.c);
    printf("line2 : %fx + %fy = %f\n", l2.a, l2.b, l2.c);
    printf("%f %f\n", p.x, p.y);
    return 0;
}