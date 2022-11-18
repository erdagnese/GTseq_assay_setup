# GTseq_assay_setup
## Python and Rmarkdown scripts to create Primers for a GTseq assay
The scripts in this repository are meant to take SNPs from RADseq data, previously identified by variable methods and create a list of primers to order for a GTseq panel
They are run in order. 
The first ***1-Seal_SS_test_SNP_filter.py*** requires input of a large VCF file from RADseq data from Salish Sea harbor seal scats, and the output is used in the second ***2-SNPs_stats_selection.Rmd***
The second script also processes directly beagle files from a global dataset of harbor seal RADseq data from a few individuals in each population and the Pacific harbor seal subset.
Only the shared SNPs between the Salish Sea harbor seals and the Pacific harbor seal dataset.
The third script ***3-bedtools_flankingSeqs.py***
The VCF files and beagle files are too large to include on Git, and the reference genome required for the bedtools script is located here https://www.ncbi.nlm.nih.gov/assembly/GCF_004348235.1/

Some of the actions must occur outside of scripts, it requires BatchPrimer3 online here https://probes.pw.usda.gov/cgi-bin/batchprimer3/batchprimer3.cgi?PRIMER_TYPE=4&CLEAR_FORM=yes

Then the outputs exported from BatchPrimer3 require renaming as .csv files for Rmarkdown script ***4-SNP_Primer_selection.Rmd*** which will output the final set of primers to order from IDT
