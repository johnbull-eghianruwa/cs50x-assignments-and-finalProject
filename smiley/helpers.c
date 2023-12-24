#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    for(int row =0; < width; row++){
        for(int col = 0; column < height; col++){
            if(image[col][row].rgbtBlue == 0 &&
            image[col][row].rgbtGreen == 0 &&
            image[col][row].rgbtRed == 0)
                image[col][row].rgbtBlue = 27;
                image[col][row].rgbtGreen = 0;
                image[col][row].rgbtRed = 255;        }
    }
}
