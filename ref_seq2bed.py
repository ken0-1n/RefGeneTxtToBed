#! /usr/local/bin/python

import sys, gzip
import os.path
import subprocess
from subprocess import Popen, PIPE


def merge_bed(outputPath, BEDToolsPath, target):
     
    print('---'+target+"---")

    with open(outputPath+"/refGene.coding."+target+".tmp2.bed", 'w') as hout:
        try:
            sort_cmd_list = [BEDToolsPath+"/sortBed", '-i', outputPath+"/refGene.coding."+target+".tmp.bed"]
            completed = subprocess.run(sort_cmd_list, stdout=hout)
        except subprocess.CalledProcessError as err:
            print('ERROR:', err)
        else:
            print('returncode:', completed.returncode)

    with open(outputPath+"/refGene.coding."+target+".bed", 'w') as hout:
        try:
            merge_cmd_list = [BEDToolsPath+"/mergeBed", '-c','4', '-o', 'collapse', '-i', outputPath+"/refGene.coding."+target+".tmp2.bed"]
            completed = subprocess.run(merge_cmd_list, stdout=hout)
        except subprocess.CalledProcessError as err:
            print('ERROR:', err)
        else:
            print('returncode:', completed.returncode)


if (len(sys.argv) != 3): 
    print ('')
    print ('Usage: # python %s filename refGene.txt.gz bedtools_path' % sys.argv[0])
    print ('')
    quit()

scriptDir = os.path.dirname(sys.argv[0])
if scriptDir == "":  scriptDir = "."

inputFile = sys.argv[1]
BEDToolsPath = sys.argv[2]
outputPath = os.path.dirname(inputFile)
if outputPath == "":  outputPath = "."

target_chr_list = [
    'chr1',
    'chr2',
    'chr3',
    'chr4',
    'chr5',
    'chr6',
    'chr7',
    'chr8',
    'chr9',
    'chr10',
    'chr11',
    'chr12',
    'chr13',
    'chr14',
    'chr15',
    'chr16',
    'chr17',
    'chr18',
    'chr19',
    'chr20',
    'chr21',
    'chr22',
    'chrX',
    'chrY',
    'chrM'
    ]

h3PUTR = open(outputPath + "/refGene.coding.3putr.tmp.bed","w")
h5PUTR = open(outputPath + "/refGene.coding.5putr.tmp.bed","w")
hEXON = open(outputPath + "/refGene.coding.exon.tmp.bed","w")
hINTRON = open(outputPath + "/refGene.coding.intron.tmp.bed","w")

with gzip.open(inputFile, 'rt') as hIN:
    for line in hIN:
        F = line.rstrip('\n').split('\t')

        category = F[1]
        if not category.startswith('NM'): continue
    
        chrom = F[2]
        if chrom not in target_chr_list: continue

        strand = F[3]
        cdsStart = int(F[6])
        cdsEnd = int(F[7])
        exonNum = int(F[8])
        starts = F[9].split(',')
        ends = F[10].split(',')
        symbol = F[12]

        # chr = chr.replace('chr', '')

        for i in range(0, len(starts) - 1):
            if (min(int(ends[i]), cdsStart) - int(starts[i]) > 0): 
                if (strand == "+"):
                    # out 5PUTR
                    print(chrom +"\t"+ starts[i] +"\t"+ str(min(int(ends[i]), cdsStart)) +"\t"+ symbol +"("+ category +")", file=h5PUTR)
                else:
                    # out 3PUTR
                    print(chrom +"\t"+ starts[i] +"\t"+ str(min(int(ends[i]), cdsStart)) +"\t"+ symbol +"("+ category +")", file=h3PUTR)

            if (min(int(ends[i]), cdsEnd) - max(int(starts[i]), cdsStart) > 0):
                # exon
                print(chrom +"\t"+ str(max(int(starts[i]), cdsStart)) +"\t"+ str(min(int(ends[i]), cdsEnd)) +"\t"+ symbol +"("+ category+ ")", file=hEXON)
        
            if (int(ends[i]) - max(cdsEnd, int(starts[i])) > 0):
                if (strand == "+"):
                    print(chrom +"\t"+ str(max(cdsEnd, int(starts[i]))) +"\t"+ ends[i] +"\t"+ symbol +"("+ category +")", file=h3PUTR)
                else:
                    print(chrom +"\t"+ str(max(cdsEnd, int(starts[i]))) +"\t"+ ends[i] +"\t"+ symbol +"("+ category +")", file=h5PUTR)
                
        for i in range(1, len(starts) - 1):
            print(chrom +"\t"+ ends[i - 1] +"\t"+ starts[i] +"\t"+ symbol +"("+ category +")", file=hINTRON)

h3PUTR.close()
h5PUTR.close()
hEXON.close()
hINTRON.close()

merge_bed(outputPath, BEDToolsPath, "exon")
merge_bed(outputPath, BEDToolsPath, "intron")
merge_bed(outputPath, BEDToolsPath, "3putr")
merge_bed(outputPath, BEDToolsPath, "5putr")

os.remove(outputPath + "/refGene.coding.3putr.tmp.bed")
os.remove(outputPath + "/refGene.coding.5putr.tmp.bed")
os.remove(outputPath + "/refGene.coding.exon.tmp.bed")
os.remove(outputPath + "/refGene.coding.intron.tmp.bed")
os.remove(outputPath + "/refGene.coding.3putr.tmp2.bed")
os.remove(outputPath + "/refGene.coding.5putr.tmp2.bed")
os.remove(outputPath + "/refGene.coding.exon.tmp2.bed")
os.remove(outputPath + "/refGene.coding.intron.tmp2.bed")

