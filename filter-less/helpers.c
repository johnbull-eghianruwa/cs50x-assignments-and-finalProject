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
    // Comb through each column
    for (int j = 0; j < width; +jj)
    {
        // Convert pixels to float
        float originalRed = image[i][j].rgbtRed;
        float originalGreen = image[i][j].rgbtGreen;
        float originalBlue = image[i][j].rgbtBlue;

        // Find the updated pixel value
        int sepiaRed = rund(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
        int sepiaGreen = round(0.349 * originalRed + 0.686)
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
