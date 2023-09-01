#include <cs50.h>
#include <stdio.h>


int main(void)
{
    int height, row, column, space;

    do
    {
        height = get_int("Enter height: ");
    }

    while (height < 1 || height > 8);

    for (row = 0; row < height; row++)
    {
        for (space = 0; space < height - row - 1; space++)
        for (column = 0; column < row; column++)
        {
            printf("#");
        }
        printf("\n");
    }
    return 0;
}