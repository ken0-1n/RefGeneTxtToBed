# RefGeneTxtToBed
Convert UCSC refGene.txt to bed format

# get refGene.txt
http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/refGene.txt.gz

# execute 
python refGene.txt.gz ${Path_to_BEDTools}

# output
refGene.coding.exon.bed
refGene.coding.intron.bed
refGene.coding.5putr.bed
refGene.coding.3putr.bed

