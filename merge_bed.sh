#/bin/bash

PATH_TO_BEDTOOLS=$1

${PATH_TO_BEDTOOLS}/mergeBed -i refGene.coding.exon.tmp.bed   -nms | ${PATH_TO_BEDTOOLS}/sortBed -i stdin > refGene.coding.exon.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
  exit 1
fi
${PATH_TO_BEDTOOLS}/mergeBed -i refGene.coding.intron.tmp.bed -nms | ${PATH_TO_BEDTOOLS}/sortBed -i stdin > refGene.coding.intron.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
  exit 1
fi
${PATH_TO_BEDTOOLS}/mergeBed -i refGene.coding.5putr.tmp.bed  -nms | ${PATH_TO_BEDTOOLS}/sortBed -i stdin > refGene.coding.5putr.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
  exit 1
fi
${PATH_TO_BEDTOOLS}/mergeBed -i refGene.coding.3putr.tmp.bed  -nms | ${PATH_TO_BEDTOOLS}/sortBed -i stdin > refGene.coding.3putr.bed
if [ ${PIPESTATUS[0]} -gt 0 -a ${PIPESTATUS[1]} -gt 0 ]; then
  exit 1
fi

