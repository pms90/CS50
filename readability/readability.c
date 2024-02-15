#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_index(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Text: ");

    // Contando letras, palabras, sentencias
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // index: Coleman-Liau index
    int index = calculate_index(letters, words, sentences);

    // Prints
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Contar lLetras
int count_letters(string text)
{
    int count = 0;

    int N = strlen(text);
    for (int i = 0; i < N; i++)
    {
        if (isalpha(text[i]))
        {
            count++;
        }
    }
    return count;
}

// Contar palabras (espacios)
int count_words(string text)
{
    int count = 1;

    int N = strlen(text);
    for (int i = 0; i < N; i++)
    {
        if (isspace(text[i]))
        {
            count++;
        }
    }
    return count;
}

// Contar sentencias (segun puntuacion)
int count_sentences(string text)
{
    int count = 0;

    int N = strlen(text);
    for (int i = 0; i < N; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            count++;
        }
    }
    return count;
}

// Calcular Coleman-Liau index
int calculate_index(int letters, int words, int sentences)
{
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    return index;
}

