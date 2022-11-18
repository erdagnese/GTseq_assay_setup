# Identifying SNPs in the VCF file of SS seal scats from Dietmar's lab which have been processed using FreeBayes
# Variant calling has already been done to create the Variant call format (VCF) file
# they are the substrate for further analyses

# take a look at the file
from distutils.core import setup

from msvcrt import kbhit


less freebayes_seals.vcf
# q to exit

# look at the header
grep "##FORMAT" freebayes_seals.vcf

# check to filter SNPs and Indels
# no sure if this is already done or not on this data
# count the number of variants we have
grep -vc '#' freebayes_seals.vcf
# 250448


vcftools --vcf freebayes_seals.vcf --remove-indels --recode --recode-INFO-all --out noindelseals.vcf
# all the SNPs were retained so there should not be any indels in there

# filter by quality 20 and count again
vcffilter -f  "QUAL >20" freebayes_seals.vcf  | grep -vc '#'
# 147836

vcftools --vcf freebayes_seals.vcf --max-missing 0.1 --mac 2 --minQ 20 --recode --recode-INFO-all --out raw.g2mac2
# so we called vcftools, gave it a vcf file, --max-missing 0.1 = keep only variants that have been successfully genotypes in 10% of individuals
# --mac 3 = minor allele count of 2; --minQ 15 = minimum quality score or 15 ; --record-INFO-all keeps all the info flags from the old vcf file in the new one
# and --out is the name of the output file
# this removed most of the data - 60832 of 250448

# filter for minimum depth for a gentype call
vcftools --vcf raw.g2mac2.recode.vcf --minDP 10 --recode --recode-INFO-all --out raw.g1mac2dp10 
# --minDP record genotypes that have less than 10 reads
# kept all 67096 - good

# filter out indivduals that didn't sequence well
vcftools --vcf raw.g1mac2dp10.recode.vcf --missing-indv
# kept all individuals

# this creates an output called out.imiss
cat out.imiss
# this kept them all - good
# highest missing is PV.26 with 76.8% missing

# visualize with a histogram
mawk '!/IN/' out.imiss | cut -f5 > totalmissing
gnuplot << \EOF 
set terminal dumb size 120, 30
set autoscale 
unset label
set title "Histogram of % missing data per individual"
set ylabel "Number of Occurrences"
set xlabel "% of missing data"
#set yr [0:100000]
binwidth=0.01
bin(x,width)=width*floor(x/width) + binwidth/2.0
plot 'totalmissing' using (bin($1,binwidth)):(1.0) smooth freq with boxes
pause -1
EOF

# most have individuals are missing more than 50% of data
# create list of indiv with more than 80% missing
mawk '$5 > 0.8' out.imiss | cut -f1 > lowDP.indv


# now with list, add that to the VCFtools filtering step
vcftools --vcf raw.g1mac2dp10.recode.vcf --remove lowDP.indv --recode --recode-INFO-all --out raw.g1mac2dp10lm

# so now that removed all but 15 individuals but kept all the sites

# now restrict the data to variants called in a high percentage of individuals and fiter by mean depth of genotypes
vcftools --vcf raw.g1mac2dp10lm.recode.vcf --max-missing 0.4 --maf 0.4 --recode --recode-INFO-all --out DP3g40maf40 
# this applied a genotype rate across individuals (40%) - do this by population when there at muliple localities
# at 20% MAF it left with 13857 SNPs out of 67096
# at 30% MAF it kept 9533 SNPs, so let's use that one
# at 40% MAF it kept 4081 out of possible 60832 sites
# let's pull out only SNPs and remove the indels
vcftools --vcf DP3g40maf40.recode.vcf --remove-indels --recode --recode-INFO-all --out snps40maf40
# kept them all

# need to rename all the chromosomes - this can do it for a list, but we have a lot, so decided to pull it into R as is and change the names in R
awk '{gsub(/ML169390.1/, "NW_022589704.1"); 
print;}' snps40maf30.recode.vcf > filtered_newchr.vcf

# pull snps40maf30.recode.vcf  into R to visualize what is left and pull out one from each region of the genome for primer design
# in R narrow down SNPs to ~2k and then prep the list to go into bedtools for next steps
# need to create a bed file with positions in R see SNPs_stats_selection.Rmd

###### reference genome processing

# so we are going to try to do it with bedtools - open new terminal - see bedtools_flankingSeqs.py
wget https://github.com/arq5x/bedtools2/releases/download/v2.29.1/bedtools-2.29.1.tar.gz
tar -zxvf bedtools-2.29.1.tar.gz
cd bedtools2
make




