#! /usr/local/bin/python

import sys, gzip
import os.path
import subprocess
from subprocess import Popen, PIPE

if (len(sys.argv) != 3): 
    print ''
    print 'Usage: # python %s filename refGene.txt.gz bedtools_path' % sys.argv[0]
    print ''
    quit()

scriptDir = os.path.dirname(sys.argv[0])
if scriptDir == "":  scriptDir = "."
print scriptDir

inputFile = sys.argv[1]
BEDToolsPath = sys.argv[2]
outputPath = os.path.dirname(inputFile)
if outputPath == "":  outputPath = "."

h3PUTR = open(outputPath + "refGene.coding.3putr.tmp.bed","w")
h5PUTR = open(outputPath + "refGene.coding.5putr.tmp.bed","w")
hEXON = open(outputPath + "refGene.coding.exon.tmp.bed","w")
hINTRON = open(outputPath + "refGene.coding.intron.tmp.bed","w")

scaffold_list= [
        'chr4_ctg9_hap1',
        'chr6_apd_hap1',
        'chr6_cox_hap2',
        'chr6_dbb_hap3',
        'chr6_mann_hap4',
        'chr6_mcf_hap5',
        'chr6_qbl_hap6',
        'chr6_ssto_hap7',
        'chr17_ctg5_hap1',
        'chr1_gl000191_random',
        'chr1_gl000192_random',
        'chr4_gl000193_random',
        'chr4_gl000194_random',
        'chr7_gl000195_random',
        'chr17_gl000205_random',
        'chr19_gl000209_random',
        'chrUn_gl000211',
        'chrUn_gl000212',
        'chrUn_gl000213',
        'chrUn_gl000215',
        'chrUn_gl000218',
        'chrUn_gl000219',
        'chrUn_gl000220',
        'chrUn_gl000222',
        'chrUn_gl000223',
        'chrUn_gl000227',
        'chrUn_gl000228',
        'chrUn_gl000241'
        ]

hIN = gzip.open(inputFile, 'r')
for line in hIN:
    F = line.rstrip('\n').split('\t')

    category = F[1]
    if not category.startswith('NM'): continue
    
    chr = F[2]
    if chr in scaffold_list: continue

    strand = F[3]
    cdsStart = int(F[6])
    cdsEnd = int(F[7])
    exonNum = int(F[8])
    starts = F[9].split(',')
    ends = F[10].split(',')
    symbol = F[12]

    chr = chr.replace('chr', '')

    for i in range(0, len(starts) - 1):
        if (min(int(ends[i]), cdsStart) - int(starts[i]) > 0): 
            if (strand == "+"):
                # out 5PUTR
                print >> h5PUTR, chr +"\t"+ starts[i] +"\t"+ str(min(int(ends[i]), cdsStart)) +"\t"+ symbol +"("+ category +")"
            else:
                # out 3PUTR
                print >> h3PUTR, chr +"\t"+ starts[i] +"\t"+ str(min(int(ends[i]), cdsStart)) +"\t"+ symbol +"("+ category +")"

        if (min(int(ends[i]), cdsEnd) - max(int(starts[i]), cdsStart) > 0):
            # exon
            print >> hEXON, chr +"\t"+ str(max(int(starts[i]), cdsStart)) +"\t"+ str(min(int(ends[i]), cdsEnd)) +"\t"+ symbol +"("+ category+ ")"
        
        if (int(ends[i]) - max(cdsEnd, int(starts[i])) > 0):
            if (strand == "+"):
                print >> h3PUTR, chr +"\t"+ str(max(cdsEnd, int(starts[i]))) +"\t"+ ends[i] +"\t"+ symbol +"("+ category +")"
            else:
                print >> h5PUTR, chr +"\t"+ str(max(cdsEnd, int(starts[i]))) +"\t"+ ends[i] +"\t"+ symbol +"("+ category +")"
                
    for i in range(1, len(starts) - 1):
        print >> hINTRON, chr +"\t"+ ends[i - 1] +"\t"+ starts[i] +"\t"+ symbol +"("+ category +")"


hIN.close()
h3PUTR.close()
h5PUTR.close()
hEXON.close()
hINTRON.close()

cmd_list = ['bash', scriptDir + '/merge_bed.sh', BEDToolsPath, outputPath]
proc = subprocess.Popen(cmd_list, stderr=subprocess.PIPE)
print 'return: %d' % (proc.wait(), )
print 'stderr: %s' % (proc.stderr.readlines(), )

