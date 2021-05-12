typedef struct point{
    float x , y ;
} point;

int main()
{
    point y = {0 , 1};
    y.x = 5 ;
    printf("y = (%f , %f)", y.x , y.y) ;
    return 0 ;
}