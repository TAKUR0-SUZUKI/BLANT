#include "structs.h"
#define TARGET_EDGE_DENSITY 0.5
// fakeN is the number of nodes inside the community I TELL the measure

// Because of the nature of how I implemented faster rejects, most of the time 
// its not the actual true number of nodes in the community

double IntraEdgeDensity(COMMUNITY *C, int fakeN){
    if(fakeN < 2)
	return 0;
    return C->edgesIn / (fakeN *(fakeN - 1) / 2.0);
}

double InterEdgeDensity(COMMUNITY *C, int fakeN){
    int tot = C->G->n - fakeN;
    //printf("tot = %d, edgesOut = %d\n", tot, edgesOut);
    return (double)C->edgesOut/(fakeN * tot);
}

double NewmanAndGirvan(COMMUNITY * C, int fakeN){
    // Eq 15 on Pg 16 on the pdf viewer
   
    // TODO: Double check what exactly is needed
    return 0;
    //return C->inEdges/C->gDegree - (cDegree/(2.0*gDegree) * cDegree/(2.0*gDegree));
}

double Conductance(COMMUNITY * C, int fakeN){
     return (double)(C->edgesOut/(C->edgesOut + C->edgesIn));
}

double HayesScore(COMMUNITY *C, int fakeN){ 
#if DEBUG
    printf("Hayes Com %d, inEdges = %d, C->n = %d\n", C->id, C->edgesIn, fakeN);
#endif
    if(fakeN < 2){
	return 0;
    }
    double eps = C->edgesIn / ((fakeN * (fakeN-1))/2.0); 
    if(eps <= TARGET_EDGE_DENSITY){
    #if VERBOSE > 2
	printf("eps too low %f\n", eps);
    #endif
	return 0;
    }
    else{
    #if VERBOSE > 2
	printf("Result = %g\n", C->edgesIn * eps * TARGET_EDGE_DENSITY/eps);
    #endif
       return C->edgesIn*eps * (TARGET_EDGE_DENSITY/eps); // to down-weight if eps is above the target
    }
}

double Modularity(COMMUNITY * C, int fakeN){
    // TODO: Actually implement modularity
    return IntraEdgeDensity(C, fakeN);
}


