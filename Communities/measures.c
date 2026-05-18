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
    
    return (fakeN == 0 || tot == 0) ? 0 : (double)C->edgesOut/(fakeN * tot);
}

double NewmanAndGirvan(PARTITION * P, COMMUNITY * C, int fakeN){
    int edgeCount = CommunityEdgeCount(C);  
    double firstTerm = edgeCount / P->G->n;
    double secondTerm = (edgeCount + CommunityEdgeOutwards(P, C)) / (2 * P->G->n);
    double ans = firstTerm - (secondTerm * secondTerm); 
    //printf("edgeCount = %d, firstTerm = %f, secondTerm = %f, ans = %f\n", edgeCount, firstTerm, secondTerm, ans); 
    return ans;
}

double Expansion(PARTITION * P, COMMUNITY * C, int fakeN){
    // Always does trivial solution of making one big community
    // Horrible objective function
    int eOut = CommunityEdgeOutwards(P, C); 
    int eIn = CommunityEdgeCount(C); 
    return eOut + eIn == 0 ? 9999999 : (double)(eOut / (eOut + eIn));  
}

double NormalizedCut(PARTITION * P, COMMUNITY * C, int fakeN){
    // Also always does trivial solution
    int eIn = CommunityEdgeCount(C);
    int eOut = CommunityEdgeOutwards(P, C);
    int denom1 = 2 * eIn + eOut; 
    int denom2 = 2 * (P->G->n - eIn) + eOut;
    if(denom1 == 0 || denom2 == 0){
	return 99999;
    }
    return (double)(eOut / (2 * eIn + eOut)) + (double)(eOut / (2 * (P->G->n - eIn) + eOut));
}

double Conductance(PARTITION * P, COMMUNITY * C, int fakeN){
     double denom = C->edgesIn < (P->G->numEdges - C->edgesIn) ? C->edgesIn : P->G->numEdges - C->edgesIn;  
     return denom == 0 ? 99999 : (double)(C->edgesOut/denom);
}

double HayesScore(PARTITION * P, COMMUNITY *C, int fakeN){ 
#if DEBUG
    printf("Hayes Com %d, inEdges = %d, C->n = %d\n", C->id, C->edgesIn, fakeN);
#endif
    if(fakeN < 2){
	return 0;
    }
    return C->edgesIn * C->edgesIn / ((fakeN * (fakeN-1))/2.0);
    
}

double Modularity(PARTITION * P, COMMUNITY * C, int fakeN){
    // TODO: Actually implement modularity
    return IntraEdgeDensity(P, C, fakeN);
}


