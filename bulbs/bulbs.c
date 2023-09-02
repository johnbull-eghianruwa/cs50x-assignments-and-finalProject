#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // Prompt user for input
    string message = get_string("Enter message here: ");

    // Iterate through each character of the string
    for (int i = 0,  number = strlen(message); i < number; i++)
    {
        int binary[] = {0, 0, 0, 0, 0, 0, 0, 0};

        // Convert the character into ASCII
        int decimal = message [i];

        // Convert the  ASCII into binary
        int j = 0;

        while (decimal > 0)
        {
            binary[j] = decimal % 2;
            decimal = decimal / 2;
            j++;
        }
        // print the binary reverse
        for (int k = BITS_IN_BYTE - 1; k >= 0; k--)
        {
            print_bulb(binary[k]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
