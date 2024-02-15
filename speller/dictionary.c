// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 150000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int index = hash(word);   // valor del hash (no necesariamente unico)

    // table[index] corresponde a la lista de ese nodo de la tabla hash
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(word, cursor->word) == 0)  // Comparacion
        {
            return true;
        }
    }


    return false;    // (si no se encuentra la palabra en la lista)
}

// Hashes word to a number

unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hash_value = 0;
    unsigned int m = 10;       // multiplicador
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value += (m * tolower(word[i]));
        m += 1;   // cambiar el multiplicador pretende reducir las posibles coliciones
    }
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL){return false;}

    char word[LENGTH + 1]; // 1 garantizaria el \n si es que no se tomo en cuenta en LENGTH

    while (fscanf(file, "%s", word) != EOF) // scaneo
    {
        node *nodo = malloc(sizeof(node));
        if (nodo == NULL)
        {
            fclose(file);
            return false;  // caso en que no alcanza la memoria para crear un nodo
        }

        strcpy(nodo->word, word);

        unsigned int hash_value = hash(word);  // obtener valor hash

        // agregar nodo en la hash table
        nodo->next = table[hash_value];
        table[hash_value] = nodo;
    }
    fclose(file);
    return true; // si todo ok
}


// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int count = 0;

    for (int i = 0; i < N; i++)
    {
        for (node *cursor = table[i]; cursor != NULL; cursor=cursor->next)
        {
            count++;
        }
    }
    return count;
}


// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)   // Recorrer hash tablee
    {
        node *cursor = table[i];   //table[i]: primer nodo
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp); // liberar nodo
        }
    }
    return true;
}

