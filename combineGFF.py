#!/usr/bin/env python
import sys
import re

################################################################
# This script will create a file to demark and label coding regions for mitoSppIDer.
#
#Input: output name, text file key of gff files
#Key format: ReferenceName  gffFileName.gff
#The "ReferenceName" should be the same as used to build the combo fasta
#The "gffFileName.gff" is a gff formatted file with the regions you wish to plot.
#
################################################################

comboGFFName = sys.argv[1]
listName = sys.argv[2]

outGFF = open(comboGFFName, 'w')
outGFF.write("Species\tStart\tEnd\tMidpoint\tName\n")
list = open(listName, 'r')
species = list.readlines()
for spc in species:
    spc = spc.strip().split('\t')
    uniID = spc[0]
    gffName = spc[1]
    spcGFF = open(gffName, 'r')
    lines = spcGFF.readlines()
    for line in lines[3:]:
        lineInfo = line.strip().split('\t')
        type = lineInfo[2]
        start = lineInfo[3]
        end = lineInfo[4]
        length = int(end)-int(start)
        midpoint = int(start)+(length/2)
        extraInfo = lineInfo[8]
        nameInfo = extraInfo.split(";")[0]
        name = nameInfo.split("=")[1].split(' ')[0]
        if type == "CDS":
            outGFF.write(uniID+"\t"+start+"\t"+end+"\t"+str(midpoint)+"\t"+name+"\n")


