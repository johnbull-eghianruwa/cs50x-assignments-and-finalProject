#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // GET INPUT OF THE HEIGHT
    int height;
    do
    {
        height = get_int("height: ");
    }
    while (height < 1 || height > 8);

    // PRINT DESIRED PYRAMID HEIGHT
    for (int i = 0; i < height; i++)
    {
        // SET PERIMETERS FOR THE COLUMNS TO RIGHT
        for (int j = 0; j < height+i+3; j++)
        {
             printf("#");
        }
    }   printf(" ");
}