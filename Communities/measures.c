#include "structs.h"
#include "measures.h"
#define TARGET_EDGE_DENSITY 0.5
// fakeN is the number of nodes inside the community I TELL the measure

// Because of the nature of how I implemented faster rejects, most of the time 
// its not the actual true number of nodes in the community

double IntraEdgeDensity(PARTITION * P, COMMUNITY *C, int fakeN){
    if(fakeN < 2)
	return 0;
    return C->edgesIn / (fakeN *(fakeN - 1) / 2.0);
}

double InterEdgeDensity(PARTITION * P, COMMUNITY *C, int fakeN){
    int tot = C->G->n - fakeN;
    //printf("tot = %d, edgesOut = %d\n", tot, edgesOut);
    return (double)C->edgesOut/(fakeN * tot);
}

double NewmanAndGirvan(PARTITION * P, COMMUNITY * C, int fakeN){
    // Technically faster rejects don't work for this because we need actual information 
    // for the edges, so I had to make a work around for this...
   
    double edgeCount = CommunityEdgeCount(C);  
    double firstTerm = edgeCount / P->G->n;
    double secondTerm = (edgeCount + CommunityEdgeOutwards(P, C)) / (2 * P->G->n);
    //printf("edgeCount = %f, firstTerm = %f, secondTerm = %f\n", edgeCount, firstTerm, secondTerm); 
    return firstTerm - (secondTerm * secondTerm);
}

double Conductance(PARTITION * P, COMMUNITY * C, int fakeN){
     return (double)(C->edgesOut/(C->edgesOut + C->edgesIn));
}

double HayesScore(PARTITION * P, COMMUNITY *C, int fakeN){ 
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

double Modularity(PARTITION * P, COMMUNITY * C, int fakeN){
    // TODO: Actually implement modularity
    return IntraEdgeDensity(P, C, fakeN);
}


