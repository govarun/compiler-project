
struct node{
    int data ;
    struct node* next ;
};

struct node* head;


void print_list()
{
    struct node* curr = head ;
    while(curr != NULL)
    {
        printf("%d ", (curr -> data)) ;
        curr = (curr -> next) ;
    }
    printf("\n") ;
    return ;
}

void add_start(int val)
{
    struct node* new_node = (struct node*)malloc(sizeof(struct node)) ;
    (new_node -> next) = (head) ;
    (new_node -> data) = val ;
    head = new_node ;
    return ;
}

void add_end(int val)
{
    struct node* curr = head ;
    struct node* new_node = (struct node*)malloc(sizeof(struct node)) ;
    struct node* next  ; // there should be no error because of this
    (new_node -> data) = val ;
    if(curr == NULL)
    {
        head = new_node ;
        (new_node -> next) = NULL ;
        return ;
    }
    next = (curr -> next) ;

    while(next != NULL)
    {
        curr = next ;
        next = (next -> next) ;
        
    }

    (curr -> next) = new_node ;
    (new_node -> next) = NULL ;
    return ;
}

void add_after(int key , int val)
{
    struct node* curr = head ;
    struct node* new_node = (struct node*)malloc(sizeof(struct node)) ;
    (new_node -> data) = val ;

    while(curr != NULL)
    {
        if((curr -> data) == key)
        {
            (new_node -> next) = (curr -> next) ;
            (curr -> next) = (new_node) ;
            return ;
        }  
        else
            curr = (curr -> next) ; 
    }
    printf("key = %d : not present\n", key) ;
    return ;

}

void del_start()
{
    struct node* curr = head ;
    if(curr == NULL)
    {
        printf("empty_list\n") ;
        return ;
    }
    head = (curr -> next) ;
    free(curr) ;

    //printf("address deleted = %d, val stored = %d\n", curr , (curr -> data)) ;
    // uncomment this to check if free has worked : most probably will give garbage val

    return ;
}

void del_end()
{
    struct node* curr = head ;
    struct node* next ;
    struct node* next_node ;
    if(curr == NULL)
    {
        printf("empty_list\n") ;
        return ;
    }

    next_node = (curr -> next) ;
    if(next_node == NULL)
    {
        head = NULL ;
        free(curr) ;
        return ;
    }

    while((next_node -> next) != NULL)
    {
        curr = next_node ;
        (next_node) = (next_node -> next) ;
    }
    (curr -> next) = NULL ;
    free(next_node) ;
    return ;
}

void del_val(int val)
{
    struct node* prev = head , *curr ;
    if(prev == NULL)
    {
        printf("element not present\n") ;
        return ;
    }
    if((prev -> data) == val)
    {
        head = (prev -> next) ;
        free(prev) ;
        return ;
    }

    curr = (prev -> next) ;

    while(curr != NULL)
    {
        if((curr -> data) == val)
        {
            (prev -> next) = (curr -> next) ;
            free(curr) ;
            return ;
        }
        else
        {
            prev = curr ;
            curr = (curr -> next) ;
        }
    }
    printf("element not present\n") ;
    return ;
}

struct node* find(int val)
{
    struct node* curr = head ;
    while(curr != NULL)
    {
        if((curr -> data) == val)
        {
            return curr ;
        }
        curr = (curr -> next) ;
    }
    printf("element not present\n") ;
    return NULL;
}

int main()
{
    head = NULL;

    add_end(3) ;
    print_list() ;

    add_end(2) ;
    print_list() ;

    add_after(3 , 4) ;
    print_list() ;

    add_after(3 , 5) ;
    print_list() ;

    del_start() ;
    print_list() ;

    del_val(4) ; // check by changing this to 5 and 4
    print_list() ;

    // printf("%d : \n", find(5)) ;
    // printf("%d : \n", find(2)) ;
    find(3) ;
    return 0 ;
}

/* expected output : 
3 
3 2 
3 4 2 
3 5 4 2 
5 4 2 
5 2 
7999592 : // these 2 values will vary
7999560 : 
element not present 

*/
