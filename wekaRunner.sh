#! /bin/bash

FULL_SET = seomset.arff
USER_SET = userset.arff
LA_NY_SET = nyla.arff

Set[1] = $FULL_SET
Set[2] = $USER_SET
Set[3] = $LA_NY_SET

for i in 1 2 3
do
    OUT = `echo ${Set[i]} | sed s/ "\.arff"//g`
    java -Xmx24G -cp weka.jar weka.classifiers.bayes.NaiveBayes -t ${Set[i]} -x 10 -i -k -c 1 > "$OUT-results.out"
done
