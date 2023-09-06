#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Comb through each row
    for (int i =  0; i < height; i++)
    {
        // Comb Through each column
        for (int j = 0; j < width; j++)
        {
            // Convert pixels to float
            float Red = image[i][j].rgbtRed;
            float Green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;

            // Find thr average value
            int average = round((Red + Green + Blue) / 3);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Comb through each row
    for (int i = 0; i < height; i++)
    {
    // Comb through each column
    for (int j = 0; j < width; j++)
    {
        // Convert pixels to float
        float originalRed = image[i][j].rgbtRed;
        float originalGreen = image[i][j].rgbtGreen;
        float originalBlue = image[i][j].rgbtBlue;

        // Find the updated pixel value
        int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
        int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
        int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);

        // Update the pixel value if sepiaRed, sepiaGreen or sepiaBlue exceeds 255
        if (sepiaRed > 255)
        {
            sepiaRed = 255;
        }
        if (sepiaGreen > 255)
        {
            sepiaGreen = 255;
        }
        if (sepiaBlue > 255)
        {
            sepiaBlue = 255;
        }
        // Update final pixel values
        image[i][j].rgbtRed = sepiaRed;
        image[i][j].rgbtGreen = sepiaGreen;
        image[i][j].rgbtBlue = sepiaBlue;
    }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Comb through each row
    for (int i = 0; i < height; i++)
    {
        // Comb through each column
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int totalRed, totalBlue, totalGreen;
            totalRed = totalBlue =
        }
    }
    return;
}
