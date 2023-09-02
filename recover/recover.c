#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unit8_t BYTE;

int main(int argc, char *argv[])
{
    // Check that the argument count is 2
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open file for reading
    FILE *input_file = fopen(argv[1], "r");

    // Check that the input_file is valid
    if (input_file == NULL)
    {
        printf("Could not  open file");
        return 2;
    }

    // Store block of 512 bytes in an array
    unsigned char buffer[512];

    // Track number of images generated
    int count_image = 0;

    // File pointer for recovered images
    FILE *output_file = NULL;

    // Char filename[8]
    char *filename = malloc(8 * sizeof(char));

    // Read the blocks of 512 bytes
    while (fread(buffer, sizeof(char), 512, input_file))
    {
        // Check if bytes indicate start of JPEG
        if (buffer[0] == oxff && buffer[1] == oxd8)
    }
}