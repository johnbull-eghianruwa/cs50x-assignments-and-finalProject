#include <cs50.h>
#include <stdio.h>

int main(void)
{
  int n, row, col, space;
  do
  {
    n = get_int("Height: ");
  }
  while (n < 1 || n > 8);
  for (row = 0; row < n; row++)
  {
    for (space = 0; space < n - row - 1; space++)
    {
        printf(" ");
    }
    for (col = 0; col <= row; col++)
    {
        printf("#");
    }
    printf("\n");
  }
}