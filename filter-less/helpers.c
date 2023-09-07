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
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            int rgbGray = round ((image[row][col].rgbtBlue + image[row][col].rgbtGreen + image[row][col].rgbtRed) / 3.0);
            image[row][col].rgbtBlue = rgbGray;
            image[row][col].rgbtGreen = rgbGray;
            image[row][col].rgbtRed = rgbGray;
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
     for (int row = 0; row < height; row++)
     {
        for (int col = 0; col < width; col++)
        {
            int sepiaRed = round(.393 * image[row][col].rgbtRed + .769 * image[row][col].rgbtGreen + .189 *image[row][col].rgbtBlue);
            int sepiaGreen = round(.349 * image[row][col].rgbtRed + .686 * image[row][col].rgbtGreen + .168 *image[row][col].rgbtBlue);
            int sepiaBlue = round(.272 * image[row][col].rgbtRed + .534 * image[row][col].rgbtGreen + .131 *image[row][col].rgbtBlue);

            image[row][col].rgbtRed = fmin(255, sepiaRed);
            image[row][col].rgbtGreen = fmin(255, sepiaGreen);
            image[row][col].rgbtBlue = fmin(255, sepiaBlue);
        }
     }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // So any pixels on the left side of the image should end up on the right; and vice versa
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width / 2; col++)
        {
            RGBTRIPLE temp = image[row][col];
            image[row][col] = image[row][width - (col + 1)];
            image[row][width - (col + 1)] = temp;
        }
    }
    return;
}
int getBlur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position)
{
    float count = 0;
    int sum = 0;
    for (int row = i - 1; row <= (i + 1); row++)
    {
        for (int col = j - 1; col  <= (j + 1); col++)
        {
            if (row < 0 || row >= height || col < 0 || col >= width)
            {
                continue;
            }
            if (color_position == RED_COLOR)
            {
                sum += image[row][col].rgbtRed;
            }
            else if (color_position == GREEN_COLOR)
            {
                sum += image[row][col].rgbtGreen;
            }
            else
            {
                sum += image[row][col].rgbtBlue;
            }
            count++;
        }
    }
    return round(sum/count);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            copy[row][col] = image[row][col];
        }
    }
    for (int row = 0; row < height; row++)
    {
        for ( int col = 0; col < width; col++)
        {
            image[row][col].rgbtRed = getBlur(row, col, height, width, copy[height][width], RED_COLOR);
            image[row][col].rgbtGreen = getBlur(row, col, height, width, copy[height][width], GREEN_COLOR);
            image[row][col].rgbtBlue = getBlur(row, col, height, width, copy[height][width], BLUE_COLOR);

        }
    }
    return;
}
