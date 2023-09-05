#include <stdio.h>
#include <cs50.h>
 #include <string.h>
 #include <math.h>

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
    else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
    {
        sentences++;
    }
   }

   float L = (float)letters / (float) words * 100;
   float S = (sentences) / (float) words * 100;
   int index = round(0.0588 * L - 0.296 * S - 15.8);

   if (index < 1)
   {
    printf("Before Grade 1+\n");
   }
   if (index > 16)
   {
    printf("Grade 16+\n");
   }
   else
   {
    printf("Grade %i\n", index);
   }
}