#include "structs.h"
#include "measures.h"

typedef struct 	{
    const char * name;
    double (*func)(COMMUNITY * C, int fakeN);
} SCORINGOPTION;

static const SCORINGOPTION scoreOpts[] = { 
    {"IntraEdgeDensity", IntraEdgeDensity},
    {"InterEdgeDensity", InterEdgeDensity},
    {"Conductance", Conductance}, 
    {"HayesScore", HayesScore}, 
};

static const int numScoreOpts = sizeof(scoreOpts) / sizeof(SCORINGOPTION);

