typedef struct point{
    int x ;
    int y ;
}   ;

struct node{
    int data ;
    node* next ;
}

int main()
{
    point p ;
    point pd = {0 , 1} ;
    p.x = 5 ;
    p.y = 10 ;
    point *q=&p ;
    (q->x) = 10 ; // wrong tokenization in this line

    struct node d , e , *f;
    (d.next)=(&e) ;
    struct* head=(&d) ;

    return ;

}