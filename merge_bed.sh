#/bin/bash

PATH_TO_BEDTOOLS=$1

${PATH_TO_BEDTOOLS}/sortBed -i refGene.coding.exon.tmp.bed   | ${PATH_TO_BEDTOOLS}/mergeBed -i stdin -c 4 -o collapse > refGene.coding.exon.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
    exit 1
fi
${PATH_TO_BEDTOOLS}/sortBed -i refGene.coding.intron.tmp.bed  | ${PATH_TO_BEDTOOLS}/mergeBed -i stdin -c 4 -o collapse > refGene.coding.intron.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
    exit 1
fi
${PATH_TO_BEDTOOLS}/sortBed -i refGene.coding.5putr.tmp.bed   | ${PATH_TO_BEDTOOLS}/mergeBed -i stdin -c 4 -o collapse > refGene.coding.5putr.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
    exit 1
fi
${PATH_TO_BEDTOOLS}/sortBed -i refGene.coding.3putr.tmp.bed   | ${PATH_TO_BEDTOOLS}/mergeBed -i stdin -c 4 -o collapse > refGene.coding.3putr.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
    exit 1
fi

