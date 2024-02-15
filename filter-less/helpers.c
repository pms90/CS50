#include "helpers.h"
#include <math.h>


int fitRange(int value); // (mi funcion)


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average; // mismo valor para todos -> gris
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed, sepiaGreen, sepiaBlue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Usando definicion dada:
            sepiaRed = fitRange(round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue));
            sepiaGreen = fitRange(round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue));
            sepiaBlue = fitRange(round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue));
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
    RGBTRIPLE temp;
    int mwidth = width / 2; // checkear caso impar
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < mwidth; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copia de imagen para usar valores originales luego
    RGBTRIPLE img_copia[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            img_copia[i][j] = image[i][j];
        }
    }

    // Filtrar
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int aux = 0;
            int R_sum = 0;
            int G_sum = 0;
            int B_sum = 0;

            // Recorrer pixels alrededor del pixel central
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    int row = i + k;
                    int col = j + l;

                    if ((row >= 0) && (row < height) && (col >= 0) && (col < width))
                    {
                        R_sum += img_copia[row][col].rgbtRed;
                        G_sum += img_copia[row][col].rgbtGreen;
                        B_sum += img_copia[row][col].rgbtBlue;
                        aux++;
                    }
                }
            }

            // Cambiar cada valor al promedio de los pixeles de alrededor
            image[i][j].rgbtRed = round((float) R_sum / aux);
            image[i][j].rgbtGreen = round((float) G_sum / aux);
            image[i][j].rgbtBlue = round((float) B_sum / aux);
        }
    }

    return;
}



int fitRange(int value)  // Evitar valores fuera de rango
{
    if (value < 0)
    {
        return 0;
    }
    else if (value > 255)
    {
        return 255;
    }
    else
    {
        return value;
    }
}