// #include <stdio.h>
int adj[5][5];

void initialize()
{
    int i = 0, j = 0;
    for (i; i < 5; i++)
    {
        for (j; j < 5; j++)
        {
            adj[i][j] = 0;
        }
    }
}
void add_edge(int u, int v)
{
    adj[u][v] = 1;
    adj[v][u] = 1;
}

void print()
{
    int i, j;
    for (i = 0; i < 5; i++)
    {
        printf("%d : ", i);
        for (j=0; j < 5; j++)
        {
            if (adj[i][j] == 1)
                printf("%d ", j);
        }
        printf("\n");
    }
}

int main()
{
    int e, u, v, i;
    printf("how many edges to add ?\n");
    scanf("%d", &e);
    initialize();
    for (i = 0; i < e; i++)
    {
        scanf("%d %d", &u, &v);
        add_edge(u, v);
    }
    print();
    return 0;
}