#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    // prmpt user for text
    string text = get_string("Type a text here: ");
    printf("%s\n", text);

    // Count the number of letters there are in the text
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= "a" && text[i] <= "z") || (text[i] >= "A" && text[i] <= "Z"))
        letters++;
    }
    printf("%i letters", letters);
}