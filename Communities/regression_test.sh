#!/bin/bash

# Currently only supporting one edgelist at a time
if [ $# -eq 0 ]; then
    echo "Please specify community to run on as an argument." 
    echo "You may optionally specify:"
    echo "			      1) -s: Set a scoring function. Default is HayesScore (refer to measures.c to see what is implemented)"
    echo "			      2) -n: Set the number of tests to run with. Default is 10 tests."
    echo "			      3) -e: Set an expected score."
    exit 
fi

PASS=0
FAIL=0
EXPECTED=""
NUMRUNS=10
EDGELIST=$1
SCORINGFUNC="HayesScore"
shift
echo "Running regression tests..."

while getopts "n:s:e:" flag; do
    case "${flag}" in
	n) echo "Running $OPTARG" times ; NUMRUNS=$OPTARG;;
	e) echo "Expected score = $OPTARG" ; EXPECTED="Final score = $OPTARG";;
	s) echo "Setting scoring function to $OPTARG"; SCORINGFUNC=$OPTARG;;
    esac
done

if [[ $EXPECTED != "" ]]; then
    echo "Set expected score to $2"
    for i in $(seq 1 $NUMRUNS); do
	OUTPUT=$(./a.out $EDGELIST -s $SCORINGFUNC 2>/dev/null)
	ACTUAL=$(echo "$OUTPUT" | grep "Final score")
	
	if [[ "$ACTUAL" =~ "$EXPECTED" ]]; then
	    echo "Run $i: PASS"
	    ((PASS++))
	else
	    echo "Run $i: FAIL ('$ACTUAL')"
	    ((FAIL++))
	fi
    done
    echo ""
    echo "Results: $PASS passed, $FAIL failed"
    exit 
else
    echo "No expected score set"
    declare -A scores
    for i in $(seq 1 $NUMRUNS); do
	OUTPUT=$(./a.out $EDGELIST -s $SCORINGFUNC 2>/dev/null)
	ACTUAL=$(echo "$OUTPUT" | grep "Final score")
	if [[ -v scores[$ACTUAL] ]]; then
	    ((scores[$ACTUAL]++))
	else
	    scores["$ACTUAL"]=1
	fi
    done
    for score in "${!scores[@]}"; do 
	 echo "  $score — ${scores[$score]}/$NUMRUNS runs"	
    done
fi
