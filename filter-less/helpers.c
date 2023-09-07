#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // So convert a pixel to grascale, we just need to make sure
    // the red, green, amd blue values are all the same value.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbGray = round ((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = rgbGray;
            image[i][j].rgbtGreen = rgbGray;
            image[i][j].rgbtRed = rgbGray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
      // sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
      // sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
     //sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue
     // As a result, we can guarantee that the resulting red, green, and blue values will be whole numbers between 0 and 255, inclusive
     for (int i = 0; i < height; i++)
     {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 *image[i][j].rgbtBlue)
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 *image[i][j].rgbtBlue)
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 *image[i][j].rgbtBlue)
        }
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
