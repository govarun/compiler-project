
int main() {
    char a = 'a';
    char b = 'b';
    int c = a, g;
    char d, e, f;
    float h = 1.3434, i;
    
    d = a + b;
    printf("%c %c %c\n", d, a, b);
    d = a - b;
    printf("%c %c %c\n", d, a, b);
    d = b - a;
    printf("%c %c %c\n", d, a, b);
    d = a / b;
    printf("%c %c %c\n", d, a, b);
    d = b / a;
    printf("%c %c %c\n", d, a, b);
    d = a * b;
    printf("%c %c %c\n", d, a, b);

    g = a + b;
    printf("%d %c %c\n", g, a, b);
    g = a - b;
    printf("%d %c %d\n", g, a, b);
    g = a / b;
    printf("%d %d %c\n", g, a, b);
    g = b / a;
    printf("%d %c %c\n", g, a, b);
    g = a * b;
    printf("%f %f %f\n", g, a, b);

    i = a + b;
    printf("%f %f %f\n", i, a, b);
    i = a - b;
    printf("%f %d %c\n", i, a, b);
    i = a / b;
    printf("%f %d %d\n", i, a, b);
    i = b / a;
    printf("%f %c %c\n", i, a, b);
    i = a * b;
    printf("%f %d %d\n", i, a, b);

    i = h + b;
    printf("%f %f %f\n", i, h, b);
    i = h - b;
    printf("%f %f %d\n", i, h, b);
    i = h / b;
    printf("%f %f %c\n", i, h, b);
    i = b / h;
    printf("%f %f %f\n", i, h, b);
    i = h * b;
    printf("%f %f %f\n", i, h, b);

}