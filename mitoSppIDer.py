__author__ = 'Quinn'

import sys, re, subprocess, time, argparse

###############################################################
# This script runs the mitoSppIDer pipeline. Which is meant for mapping short read data to a combined genome of just mitochondiral genomes (or other small genomes)
# Before running this you must make your combination reference mitochondiral genome with the script combineRefGenomes.py
# If you wish to delineate and label the coding regions you will need to create a file with information about these regions using combineGFF.py
#
# This script will map short-read data to a combination mitochondiral reference genome and parse the outputs to create a summary of
# where and how well the reads map to each species in the combinaiton reference mitochondiral genome. If you include a combination gff
# these regions will be be demarked by shaded regions on the output depth plot.
#
#Program Requirements: bwa, samtools, bedtools, R, Rpackage ggplot2, Rpackage dplyr
#Input: Output name, Combination reference mitochondrial genome, Combination reference mitochondrial gff, fastq short-read files
#
################################################################

parser = argparse.ArgumentParser(description="Run full sppIDer")
parser.add_argument('--out', help="Output prefix, required", required=True)
parser.add_argument('--ref', help="Reference Genome, required", required=True)
parser.add_argument('--r1', help="Read1, required", required=True)
parser.add_argument('--r2', help="Read2, optional")
parser.add_argument('--gff', help="Key to gff file, optional")
args = parser.parse_args()

scriptsPath = #EDIT# pathToSppIDerScripts

outputPrefix = args.out
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'w')
trackerOut.write("outputPrefix = "+args.out+"\n")
ref=args.ref
start = time.time()
def calcElapsedTime( endTime ):
    trackedTime = str()
    if 60 < endTime < 3600:
        min = int(endTime) / 60
        sec = int(endTime - (min * 60))
        trackedTime = "%s mins %s secs" % (min, sec)
    elif 3600 < endTime < 86400:
        hr = int(endTime) / 3600
        min = int((endTime - (hr * 3600)) / 60)
        sec = int(endTime - ((hr * 60) * 60 + (min * 60)))
        trackedTime = "%s hrs %s mins %s secs" % (hr, min, sec)
    elif 86400 < endTime < 604800:
        day = int(endTime) / 86400
        hr = int((endTime - (day * 86400)) / 3600)
        min = int((endTime - (hr * 3600 + day * 86400)) / 60)
        sec = int(endTime - ((day * 86400) + (hr * 3600) + (min * 60)))
        trackedTime = "%s days %s hrs %s mins %s secs" % (day, hr, min, sec)
    else:
        trackedTime = str(int(endTime)) + " secs"
    return trackedTime

trackerOut.write("ref = "+ref+"\n")

########################## BWA ###########################
bwaOutName = outputPrefix+".sam"
bwaOutFile = open(bwaOutName, 'w')
if args.r2:
    read1Name = args.r1
    read2Name = args.r2
    print("Read1 = " + read1Name + "\nRead2=" + read2Name)
    trackerOut.write("read1 = " + read1Name + "\n")
    trackerOut.write("read2 = " + read2Name + "\n")
    if args.gff:
        trackerOut.write("gff = " + args.gff + "\n")
    trackerOut.close()
    subprocess.call(["#EDIT# pathToBWA/bwa", "mem", ref, read1Name, read2Name], stdout=bwaOutFile)
else:
    read1Name = args.r1
    print("Read1="+read1Name)
    trackerOut.write("read1=" + read1Name + "\n")
    if args.gff:
        trackerOut.write("gff=" + args.gff + "\n")
    trackerOut.close()
    subprocess.call(["#EDIT# pathToBWA/bwa", "mem", ref, read1Name], stdout=bwaOutFile)
print("BWA complete")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("BWA complete\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## samtools ###########################
samViewOutQual = outputPrefix+".view.bam"
bamSortOut = outputPrefix+".sort.bam"
samViewQualFile = open(samViewOutQual, 'w')
subprocess.call(["#EDIT# pathToSAMTOOLS/samtools", "view", "-q", "1", "-bhSu",  bwaOutName], stdout=samViewQualFile)
subprocess.call(["#EDIT# pathToSAMTOOLS/samtools", "sort", samViewOutQual, "-o", bamSortOut])
print("SAMTOOLS complete")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nSAMTOOLS complete\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## bedgraph Coverage ###########################
bedOutD = outputPrefix+"-d.bedgraph"
sortOut = bamSortOut
bedFileD = open(bedOutD, 'w')
subprocess.call(["#EDIT# pathToBEDTOOLS/genomeCoverageBed", "-d", "-ibam", sortOut], stdout=bedFileD)
print("bedgraph complete")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nbedgraph complete\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## parse SAM file ###########################
subprocess.call(["#EDIT# pathToPYTHON/python", scriptsPath+"parseSamFile.py", outputPrefix])
print("Parsed SAM file")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nParsed SAM\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## plot MQ scores ###########################
subprocess.call(["#EDIT# pathToR/Rscript", scriptsPath+"MQscores_sumPlot.R", outputPrefix])
print("Plotted MQ scores")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nMQ scores plotted\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## average -d Bed ###########################
subprocess.call(["#EDIT# pathToR/Rscript", scriptsPath+"meanDepth_sppIDer-d.R", outputPrefix])
print("Found -d mean depth")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nFound -d mean depth\nElapsed time: " + elapsedTime)
trackerOut.close()

########################## make -d plot ###########################
if args.gff:
    subprocess.call(["#EDIT# pathToR/Rscript", scriptsPath+"mitoSppIDer_depthPlot-d.R", outputPrefix, args.gff])
else:
    subprocess.call(["#EDIT# pathToR/Rscript", scriptsPath+"mitoSppIDer_depthPlot-d.R", outputPrefix])
print("Plot -d complete")
currentTime = time.time()-start
elapsedTime = calcElapsedTime(currentTime)
print("Elapsed time: " + elapsedTime)
trackerOut = open(outputPrefix+"_mitoSppIDerRun.info", 'a')
trackerOut.write("\nPlot -d complete\nElapsed time: " + elapsedTime+"\n")
trackerOut.close()

