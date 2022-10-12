#! /bin/env bash
g++ compare.cpp -o compare.x

for stressfile in hardy1 hardy2 hardy3 hardy4 hardyRandomCauchy hardyRandomPiola;
do
./compare.x $stressfile
done;