struct some{
    int a;
    char b;
}
//Should not work without ; but working fine
int main(){
    struct some *var;
    var->a = 1;
    var->a += 2;
    var->a++;
    return 0;
}