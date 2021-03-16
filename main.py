from learningAlgorithms import *
from testAlgorithms import *
import random

values = []
file_object  = open('dataset_wireless.txt', 'r')
for line in file_object:
    values.append(map(float,line.strip().split(',')))

folds = stratified10FoldCrossValidationSplit(values)
percentages = []
for fold in folds:
    trainSet = list(folds)
    trainSet.remove(fold)
    trainSet = sum(trainSet, [])
    testSet = []
    for row in fold:
        tmp = list(row)
        testSet.append(tmp)
        tmp[-1] = None
    tree = decisionTreeLearning(trainSet)
    printTree(tree)
    learned = []
    for row in testSet:
        learned.append(testRow(tree,row))
    known = [row[-1] for row in fold]
    percentages.append(accuracy(known, learned))
print percentages
print('Accuratezza media: %.3f%%' % (sum(percentages)/float(len(percentages))))
