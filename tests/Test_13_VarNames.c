int main()
{
    int n1 = 5 ;
    int 1n = 6 ; // correctly tokenized !!
    int y = 'c' ;

    int _yz = 5 ;
    int y_z = 5 ;
    int x@5 = 5 ;
    int y@ = 5 ; // although correctly tokenized, but @ not detected
    int @z = 5 ;

    return ;
}

