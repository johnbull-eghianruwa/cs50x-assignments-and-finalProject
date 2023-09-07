#include "helpers.h"
#include "math.h"

#define RED_COLOR 0
#define GREEN_COLOR 1
#define BLUE_COLOR 2

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
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 *image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 *image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 *image[i][j].rgbtBlue);

            image[i][j].rgbtRed = fmin(255, sepiaRed);
            image[i][j].rgbtGreen = fmin(255, sepiaGreen);
            image[i][j].rgbtBlue = fmin(255, sepiaBlue);
        }
     }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // So any pixels on the left side of the image should end up on the right; and vice versa
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}
int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position)
{
    float count = 0;
    int sum = 0;
    for (int i = i - 1; i <= (i + 1); i++)
    {
        for (int j = j - 1; j  <= (j + 1); j++)
        {
            if (row < 0 || row >= height || j < 0 || j >= width)
            {
                continue;
            }
            if (color_position == RED_COLOR)
            {
                sum += image[i][j].rgbtRed;
            }
            else if (color_position == GREEN_COLOR)
            {
                sum += image[i][j].rgbtGreen;
            }
            else
            {
                sum += image[i][j].rgbtBlue;
            }
            count++;
        }
    }
    return round(sum/count)
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = int getBlur(i, j, height, width, copy[height][width], RED_COLOR);
            image[i][j].rgbtGreen =
            image[i][j].rgbtBlue =

        }
    }
    return;
}
