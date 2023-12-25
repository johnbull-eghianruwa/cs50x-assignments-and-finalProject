#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int initialPopulation;
    do
    {
        initialPopulation = get_int("Starting Population: ");
    }
    while (initialPopulation < 9);

    // TODO: Prompt for end size
    int targetPopulation;
    do
    {
        targetPopulation = get_int("Ending Population: ");
    }
    while (initialPopulation > targetPopulation);

    // TODO: Calculate number of years until we reach threshold
    int year = 0;

    while (initialPopulation < targetPopulation) {
        initialPopulation = initialPopulation + (initialPopulation / 3) - (initialPopulation / 4);
        year++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", year);
}
