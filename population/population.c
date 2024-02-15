#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int sp = get_int("Start size: ");
    while (sp < 9)
    {
        sp = get_int("Start size: ");
    }

    // TODO: Prompt for end size
    int ep = get_int("End size: ");
    while (ep < sp)
    {
        ep = get_int("End size: ");
    }

    // TODO: Calculate number of years until we reach threshold
    int t = 0;
    float p = (float) sp;
    while (p < ep)
    {
        p = p + (int) p / 3 - (int) p / 4;
        // printf("population: %f \n", p);
        t++;
    }

    // TODO: Print number of years
    printf("Years: %i \n", t);
}
