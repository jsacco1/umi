# umi

Preprocessing tools for unique molecular index (UMI) sequencing reads

See the [wiki](https://github.com/aryeelab/umi/wiki) for documentation

#### This fork of the *umi* package is intended to be used with [GUIDE-seq simplified library preparation protocol](https://dx.doi.org/10.17504/protocols.io.wikfccw)


The simplified GUIDE-seq protocol produces libraries that 

1. Can be run on any Illumina sequencer without tweaking the software settings (no need to export index read files for demultiplexing). You can use demultiplexed libraries (from bcl2fastq) and use only the Read1 & Read2 files for each sample to perform the analysis.

2. Contain the Unique Molecular Identifier inline with the sequenced target region. Read2 starts with the UMI.

The above changes necessitate modifying the [GUIDE-seq](https://github.com/aryeelab/guideseq) analysis workflow to accommodate the new library structure.

### NOTE: You need to run each step of the GUIDE-seq analysis [individually](https://github.com/aryeelab/guideseq#running-analysis-steps-individually).

1. Install the GUIDE-seq package. Instructions [here](https://github.com/aryeelab/guideseq#download-and-set-up-guideseq).

2. Download the UMI package from this repo and replace the umitag.py in the GUIDE-seq package with the umitag.py file from this package.

3. Start analysis with step [umitag](https://github.com/aryeelab/guideseq#umitag-reads). Since you will be working with demultiplexed fastq files, use the following command.

```
python ../umitag.py --read1_in mysample.r1.fastq --read2_in mysample.r2.fastq --read1_out mysample.r1.umitagged.fastq --read2_out mysample.r2.umitagged.fastq
```

4. Use the output files in the next step - [Consolidate](https://github.com/aryeelab/umi/wiki#3-consolidate-reads-with-the-same-molecular-index).

5. Follow the rest of the steps as in the GUIDE-seq analysis [workflow](https://github.com/aryeelab/guideseq#align-sites-to-genome).

### An automated pipeline similar to GUIDE-seq is under development. I will make a note here when the new package is available. 
