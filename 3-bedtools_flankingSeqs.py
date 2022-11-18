# this is the bed tools script for extracting flanking sequences based on snp position, and start and end which we created in the R marakdown
bedtools getfasta -fi GCF_004348235.1_GSC_HSeal_1.0_genomic.fna -bed SalishSea_seals.bed -name -fo SalishSea_seals_flankSNPs.fasta 

# okay so that worked but we need to modify the bed file input so includes the info BatchPrimer3 needs for the input: 
# should look something like this >gnl|dbSNP|rs16821171 rs=16821171|pos=187|len=613|taxid=10090|mol="genomic"|class=1|alleles="A/G"|build=123
# use this legend https://www.ncbi.nlm.nih.gov/projects/SNP/snp_legend.cgi?legend=fasta
# so we need a column that has a name created for each SNP that reads: >gnl|dbSNP|rsSequence|pos=1+pos in new 

# the fasta file needs to be modified so that the BP at pos=100 is a degenerate bp and on it's own line

fold -120 SalishSea_seals_flankSNPs.fasta > test.fasta

# see test2formateg.fasta for thes ones that work to put into batchPrimer3 2 of the 3 worked but the format is right and we need to find a way to change the BP to the right degeneracy based on the base pairs
# it doesn't work if you change all the SNP bp to "N" so we have to conditionally change the BP using a position file we created in the R markdown

# got the following answer from stackoverflow: https://stackoverflow.com/questions/29541732/using-bioperl-to-alter-nucleotides-at-specific-positions-in-fasta-file


# that didn't work 

perl -pe '$. > 1 and /^>/ ? print "\n" : chomp' SalishSea_seals_flankSNPs.fasta > outSNPs.fasta
python3
# let's try a couple other options I found on internet
from collections import defaultdict

with open('SalishSea_SNPsPosition.txt', 'r') as f:
        pos = defaultdict(list)
        for line in f:
                pos[line.strip().split('\t')[0]].append((int(line.strip().split('\t')[1]), line.strip().split('\t')[2]))

with open('outSNPs.fasta', 'r') as fasta:
        with open('SSseals_flankSNPs_corr.fasta', 'w') as out:
                for line in fasta:
                        if line.startswith(">"):
                                h = line.strip().split('>')[1]
                                s = list(next(fasta).strip())
                                if h in pos:
                                        for n in pos[h]:
                                                s[n[0]-1] = n[1]
                                        out.write('>' + h + '\n' + ''.join(s) + '\n')
                      
# yahoo that worked, finally!
exit() # get out of python
# so funny story, BatchPrimer3 only takes 500 at a time, so we need to split the output fasta that has been corrected into multiple fasta files
# there are 2843 SNPs, so there will need to be 6 fasta files with 1000 lines or less in each

awk -v size=500 -v pre=SNPbatch -v pad=1 '/^>/{n++;if(n%size==1){close(f);f=sprintf("%s.%0"pad"d",pre,n,fasta)}}{print>>f}' CopySSseals_flankSNPs_corr.fasta
# this outputs the files but without the fasta file extension so that needs to be fixed
# can do this be renaming the files in the explorer since there is only 6

