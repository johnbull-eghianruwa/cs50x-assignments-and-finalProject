#include <cs50.h>
#include <stdio.h>

int main(void)
{
  int n;
  do
  {
    n = get_int("Height: ");
  }
  while (height < 1 || height > 8)

  for (int i = 0; < height; i++)
  {
    for (int j = 0; j < i; j++)
    {
        printf("#");
    }
    printf("\n");
  }

}