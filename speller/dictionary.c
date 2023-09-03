// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Declare variables
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash the word to obtain a hash value
    hash_value = hash(word);
    node *cursor = table[hash_value];

    // Go through linked list
    while (cursor != 0)
    {
        if (strcmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unigned long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open dictionary
    FILE *file = fopen(dictionary, "r");

    // Return NULL if file cannot be opened
    if (file == NULL)
    {
        printf("Unable to open %S\n", dictionary);
        return false;
    }
    // Declare variable called word
    char word[LENGTH+];

    // Scan dictionary for string up untill EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for new node

        node *n = malloc(sizeof(node));
    // if malloc returns NULL, return false
     if (n == NULL)
    }
        return false;
    {
        // Copy word from dictionary into node
        strcopy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return size of dictionary
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    while (cursor)
    {
        node *tmp = cursor;
        cursor = cursor->next;
        free(tmp);
    }
    if (cursor == NULL)
    {
        return true;
    }
    return false;
}
