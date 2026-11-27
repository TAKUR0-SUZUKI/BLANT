S.A.K.E
(Simulated Annealing Kommunity Explorer)

To compile first do 

export LIBWAYNE_HOME={your path to BLANT starting with ~}/libwayne

Ex: 
export LIBWAYNE_HOME=~/BLANT/libwayne

Then in the communities directory

make

in your command line to compile

To run 

./a.out {Graph to run on} 

Ex:
./a.out ./communities.in

OPTIONS
-s Choose a scoring function
-p Provide a partition to start from 
-r Random seed to use (default: a fancy seed, printed as "Random seed N"), so a run can be reproduced exactly
-m Perturbation mode: swap (move a node or swap two, the default), move (move a node only), or all (move a node,
   merge two communities, or split one). Combine with -t to run several in parallel, eg -m all -t 8
-n Iteration factor: anneal for (factor x number of edges) iterations (default 60000)
-T Tolerance (like SANA's -tolerance): instead of a fixed number of iterations, stay at each temperature until the
   score settles there, so temperatures where the score is changing get more iterations and flat ones fewer.
   Smaller is slower and more careful; 0.1-0.3 works well on yeast. Overrides -n, which then only sets the batch
   size (sqrt(factor x edges) iterations per batch).
-t Run this many independent anneals in parallel (one process each, seeds N, N+1, ...) and keep the best;
   0 means one per CPU. Prints the best run's output followed by a "Best of" line listing every run's score.
   Wall time is about that of a single run, as long as there are enough cores.

Ex:
./a.out ./communities.in -t 8 -r 100
