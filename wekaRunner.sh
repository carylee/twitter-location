#! /bin/bash

FULL_SET=1234.arff
USER_SET=1234.arff
LA_NY_SET=1234.arff

Set[1]=$FULL_SET
Set[2]=$USER_SET
Set[3]=$LA_NY_SET

for i in 1 2 3
do
    OUT=`echo ${Set[i]} | sed 's/\(.*\)\..*/\1/'`
    echo $OUT
    java -Xmx24G -cp weka.jar weka.classifiers.bayes.NaiveBayes -t ${Set[i]} -x 10 -i -k -c 1 > "$OUT-results.out"
done
