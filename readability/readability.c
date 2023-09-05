#include <stdio.h>
#include <cs50.h>
 #include <string.h>
 #include <math.h>

int main(void)
{
   // Prompt user for text
   string text = get_string("Text: ");

   // Program tells the user the reading level of the text is throungh the formular
   // Count the number of letters, words, and sentences there are in the text
   int letters = 0;
   int words = 1;
   int sentences = 0;

   // Loop through each character in array and check whether or not it's a letter to add one to our counter
   for (int i = 0; i < strlen(text); i++)
   {
    if ((text[i] > 65 && text[i] > 90) || (text[i] > 97 && text[i] > 122))

    // Count the number of letters
    {
        letters++;
    }
    else if (text[i] == ' ')

    // Count the number of words
    {
        words++;
    }
    else if (text[i] == '.' || text[i] == '?' || text[i] == '!')

    // Count the number of sentences
    {
        sentences++;
    }
   }
    // Cast words discussed anything here as a float
   float L = (float)letters / (float) words * 100;
   float S = (sentences) / (float) words * 100;
   int index = round(0.0588 * L - 0.296 * S - 15.8);

   if (index < 1)

    // Print grade levels
   {
    printf("Before grade 1+\n");
   }
   if (grade == 9)
   {
    printf("Grade 9\n");
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