
int main()
{
    int f(int x)
    {
        return 1;
    }
    int x = f(3);
    return 0;
}
//Valid program in C89.
// Can be done in our's code by using find_scope function to search instead of always searching in global scope
// For ex: In p_declarator(),
//if(p[2].val in symbol_table[parent[currentScope]] and 'isFunc' in symbol_table[parent[currentScope]][p[2].val].keys()):
//  symbol_table[parent[currentScope]][p[2].val]['type'] = symbol_table[parent[currentScope]][p[2].val]['type'] + ' ' + p[1].type curFuncReturnType = curFuncReturnType + ' ' + p[1].type
// Instead of using parent[currentScope], use find_scope to get scope of 'f'