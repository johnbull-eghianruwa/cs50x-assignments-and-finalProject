#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prmpt user for text
    string text = get_string("Type a text here: ");
    printf("%s\n", text);
}