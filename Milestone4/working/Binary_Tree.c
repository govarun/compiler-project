struct node{
   int val ;
   float f_val ;
 
   struct node* left , *right ;
};
 
void insert(struct node **root , int val , float f_val)
{
   struct node * curr ;
   if((*root) == NULL)
   {
       curr = (struct node*)malloc(sizeof(struct node)) ;
       (*root) = curr ;
       (curr -> val) = val ;
       (curr -> f_val) = f_val ;
       (curr -> left) = NULL ;
       (curr -> right) = NULL ;
       return ;
   }
   if(((*root) -> val) >= val)
   {
       if(((*root)->left) == NULL)
       {
           curr = (struct node*)malloc(sizeof(struct node)) ;
           ((*root) -> left) = curr ;
           (curr -> val) = val ;
           (curr -> f_val) = f_val ;
           (curr -> left) = NULL ;
           (curr -> right) = NULL ;
           return ;
       }
       else
       {
           insert(&((*root) -> left) , val , f_val) ;
           return ;
       }
   }
   else
   {
       if(((*root)->right) == NULL)
       {
           curr = (struct node*)malloc(sizeof(struct node)) ;
           ((*root) -> right) = curr ;
           (curr -> val) = val ;
           (curr -> f_val) = f_val ;
           (curr -> left) = NULL ;
           (curr -> right) = NULL ;
           return ;
       }
       else
       {
           insert(&((*root) -> right) , val , f_val) ;
           return ;
       }
   }
}  
 
void print_tree(struct node* root)
{
   if(root == NULL)
       return ;
   print_tree(root -> left) ;
   printf("(%d, %f) ", (root -> val) , (root -> f_val)) ;
   print_tree(root -> right) ;
   return ;
}  
 
void find(struct node* root , int val)
{
   if(root == NULL)
   {
       printf("val = %d not present\n", val) ;
       return ;
   }
   if((root -> val) == val)
   {
       printf("val = %d found, with f_val = %f\n", val , root -> f_val) ;
       return ;
   }
   if((root -> val) > val)
       return find(root -> left , val) ;
   return find(root -> right , val) ;
}
 
void not_change(struct node* root , int val , float f_val)
{
   if(root == NULL)
   {
       printf("val = %d not present\n", val) ;
       return ;
   }
   if((root -> val) == val)
   {
       (root -> f_val) = f_val ;
       return ;
   }
   if((root -> val) > val)
       return not_change(root -> left , val , f_val) ;
   return not_change(root -> right , val , f_val) ;
}
 
void change(struct node** root , int val , float f_val)
{
   if((*root) == NULL)
   {
       printf("val = %d not present\n", val) ;
       return ;
   }
   if(((*root) -> val) == val)
   {
       ((*root) -> f_val) = f_val ;
       return ;
   }
   if(((*root) -> val) > val)
       return change(&((*root) -> left) , val , f_val) ;
   return change(&((*root) -> right) , val , f_val) ;
}
 
int main()
{
   struct node* root = NULL ;
   insert(&root , 8 , 3.5) ;
   insert(&root , 4 , 4.5) ;
   insert(&root , 12 , 5.5) ;
   insert(&root , 6 , 12.5) ;
   insert(&root , 5 , 10.5) ;
   insert(&root , 9 , 1.5) ;
   insert(&root , 15 , 0.5) ;
   print_tree(root) ;
   printf("\n") ;
   find(root , 9) ;
   find(root , 7) ;
   not_change(root , 9 , 12.236) ;
   find(root , 9) ;
   change(&root , 9 , 17.24) ;
   find(root , 9) ;
   return 0 ;
}
/*
(4, 4.500000) (5, 10.500000) (6, 12.500000) (8, 3.500000) (9, 1.500000) (12, 5.500000) (15, 0.500000) 
val = 9 found, with f_val = 1.500000
val = 7 not present
val = 9 found, with f_val = 12.236000
val = 9 found, with f_val = 17.240000
*/
 
 
 



