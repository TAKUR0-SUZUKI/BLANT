#ifndef MEASURES_H
#define MEASURES_H

#include "communities.h"
#include "structs.h"
double IntraEdgeDensity(COMMUNITY *C, int fakeN);
double InterEdgeDensity(COMMUNITY *C, int fakeN);
double NewmanAndGirvan(COMMUNITY *C, int fakeN);
double Conductance(COMMUNITY *C, int fakeN);
double HayesScore(COMMUNITY *C, int fakeN);
double Modularity(COMMUNITY *C, int fakeN);

#endif
