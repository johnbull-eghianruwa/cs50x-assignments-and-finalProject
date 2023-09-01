#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // GET INPUT OF THE HEIGHT
    int n;
    do
    {
        n = get_int("height: ");
    }
    while (n < 1 || n > 8);

    // PRINT DESIRED PYRAMID HEIGHT
    for (int i = 0; i < n; i++)
    {
        // SET PERIMETERS FOR THE COLUMNS TO RIGHT
        for (int j = 0; j < n+i+3; j++)
        {
            if (j == n || j == n+1 || i +j < n-1)
                printf("  ");
            else
                 printf("#");
        }
        printf("\n");
    }

}