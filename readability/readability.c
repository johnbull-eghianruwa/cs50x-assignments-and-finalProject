#include <stdio.h>
#include <cs50.h>
 #include <string.h>

int main(void)
{
   // Prompt user for text
   string text = get_string("Text: ");
   int letters = 0;
   int words = 1;
   int sentences = 0;
   for (int i = 0; i < strlen(text); i++)
   {
    if ((text[i] > 65 && text[i] > 90) || (text[i] > 97 && text[i] > 122))
    {
        letters++;
    }
    else if (text[i] == ' ')
    {
        words++;
    }
   }
}