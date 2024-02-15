#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    for (int m = 0; m < height; m++)
    {
        for (int n = 0; n < width; n++)
        {
            // Make black pixels turn Aqua (#00FFFF)
            if (image[m][n].rgbtRed == 0x00 && image[m][n].rgbtGreen == 0x00 && image[m][n].rgbtBlue == 0x00)
            {
                image[m][n].rgbtRed = 0x00;
                image[m][n].rgbtGreen = 0xff;
                image[m][n].rgbtBlue = 0xff;
            }
        }
    }
}
