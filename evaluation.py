# -*-coding:UTF-8-*-
import math
import time

__author__ = 'M'


def sgn(x):
    if x > 0:
        return 1
    else:
        return 0


def counti(trueline):
    countfr = int(trueline.split('\t')[2].split(',')[0])
    countcr = int(trueline.split('\t')[2].split(',')[1])
    countlr = int(trueline.split('\t')[2].split(',')[2])
    if (countfr + countcr + countlr) > 100:
        return 100
    else:
        return countfr + countcr + countlr


def percision(testline, trueline):
    countfp = float(testline.split('\t')[2].split(',')[0])
    countcp = float(testline.split('\t')[2].split(',')[1])
    countlp = float(testline.split('\t')[2].split(',')[2])
    countfr = float(trueline.split('\t')[2].split(',')[0])
    countcr = float(trueline.split('\t')[2].split(',')[1])
    countlr = float(trueline.split('\t')[2].split(',')[2])
    deviationf = math.fabs(countfp - countfr) / (countfr + 5)
    deviationc = math.fabs(countcp - countcr) / (countcr + 3)
    deviationl = math.fabs(countlp - countlr) / (countlr + 3)
    precision = 1 - 0.5 * deviationf - 0.25 * deviationc - 0.25 * deviationl
    return precision


def evaluate(test_lines, true_lines):
    start = time.time()
    denominator = 0.0
    numerator = 0.0
    if len(test_lines) != len(true_lines):
        print 'number of test samples is not euqal to the number of the true samples'
        return
    else:
        for index in range(len(test_lines)):
            testline = test_lines[index]
            trueline = true_lines[index]
            precision = percision(testline, trueline)
            numerator += (counti(trueline) + 1) * sgn(precision - 0.8)
            denominator += counti(trueline) + 1
        precision_final = float(numerator) / float(denominator)
    end = time.time()
    print 'evaluation fininshed with: ' + str(end - start)
    return precision_final
