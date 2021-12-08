#!/usr/bin/env python
import csv

def readfile(file):
    with open(file, 'r') as f:
        for row in csv.reader(f):
            print(row)


if __name__ == '__main__':
    readfile("./exam.csv")