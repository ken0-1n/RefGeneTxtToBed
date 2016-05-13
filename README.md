# RefGeneTxtToBed
Convert UCSC refGene.txt to bed format

## Dependency
Python (>= 2.7), 
[bedtools-2.24.0](http://code.google.com/p/bedtools/)

## Get refGene.txt from UCSC 
```
http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz
```

## Execute 
```
python ref_seq2bed.py refGene.txt.gz ${Path_to_BEDTools}
```

## Output
```
refGene.coding.exon.bed
refGene.coding.intron.bed
refGene.coding.5putr.bed
refGene.coding.3putr.bed
```
