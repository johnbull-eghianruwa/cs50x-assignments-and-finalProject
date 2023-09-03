#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // These variables represent the pyramid's height, row, column, and number of spaces respectively
    int n, row, col, space;

    // The following code check input value is from 1 and 8
    // If outside specify range the user is prompt again
    do
    {
        // Prompt user for input
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // Print the pyramid base on specify height
    for (row = 0; row < n; row++)
    {
        // Print number of spaces on row base on the width
        for (space = 0; space < n - row - 1; space++)
        {
            printf(" ");
        }

        // Print hashs base on column
        for (col = 0; col <= row; col++)
        {
            printf("#");
        }
        printf("\n");
    }
}