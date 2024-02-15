#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Validando input
    int h = 0;
    while (h < 1 || h > 8)
    {
        h = get_int("Altura: ");
    }

    // Escalera
    for (int m = 0; m < h; m++)
    {
        for (int n = h - 1; n >= 0; n--)
        {
            if (n <= m)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n"); //cambio de fila
    }
}
