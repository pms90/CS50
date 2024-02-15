#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    string message = get_string("Message: "); //input

    int N = strlen(message);

    for (int j = 0; j < N; j++)
    {
        char c = message[j];

        int decimal, cociente, residuo;

        int binario[BITS_IN_BYTE] = {0};    //se inicia con todos ceros

        decimal = (int) c;
        cociente = decimal;

        for (int i = 0; i < BITS_IN_BYTE; i++)
        {
            residuo = cociente % 2;
            binario[BITS_IN_BYTE - 1 - i] = residuo;
            cociente = cociente / 2;
        }

        for (int i = 0; i < BITS_IN_BYTE; i++)
        {
            print_bulb(binario[i]);
        }

        // Print newline despues de cada byte
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
