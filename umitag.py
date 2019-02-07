from __future__ import print_function
import os
import re
import gzip
import itertools
import argparse
import subprocess

__author__ = 'Original - Martin Aryee; Modified by Nagendra Palani (UMGC)'

# WARNING: This script works ONLY for libraries generated 
# using the protocol at https://dx.doi.org/10.17504/protocols.io.wikfccw

def fq(file):
    if re.search('.gz$', file):
        fastq = gzip.open(file, 'rb')
    else:
        fastq = open(file, 'r')
    with fastq as f:
        while True:
            l1 = f.readline()
            if not l1:
                break
            l2 = f.readline()
            l3 = f.readline()
            l4 = f.readline()
            yield [l1, l2, l3, l4]


# Create molecular ID by concatenating molecular barcode and beginning of r1 and r2 read sequences
def get_umi(r1, r2):
    molecular_barcode = r2[1][0:8]
    # extract the first 8 bases of Read2, which is the UMI

    return '%s_%s_%s' % (molecular_barcode, r1[1][35:41], r2[1][40:46])
    # Extract 6 bases from Read1 after the primer region.
    # Extract 6 bases from Read2 after the primer region. 
    # Note that I arbitrarily picked a window of base positions that will contain the genomic sequence to generate the UMI barcode. 
    # (which is 8 bp of molecular barcode + 6 bp of R1 genomic sequence + 6 bp of R2 genomic sequence)
    # You can change the window value within this function to suit your library design (longer/shorter UMI),
    # different R1 & R2 genomic sequence window lengths etc. If you change R2 window value, change the adapter trim window in 
    # ADAPTERTRIM section appropriately.

    
def umitag(read1, read2, read1_out, read2_out, out_dir):

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    r1_umitagged_unsorted_file = read1_out + '.tmp'
    r2_umitagged_unsorted_file = read2_out + '.tmp'

    # Create UMI-tagged R1 and R2 FASTQs
    r1_umitagged = open(r1_umitagged_unsorted_file, 'w')
    r2_umitagged = open(r2_umitagged_unsorted_file, 'w')

    # Because demultiplexed libraries will be run through this script, removed references to index files. Only needs R1 & R2 fastq for each sample.
    for r1,r2 in itertools.izip(fq(read1), fq(read2)):
        
        molecular_id = get_umi(r1, r2)
        # Remove default fastq read headers from fastq and add molecular id to read headers
        r1[0] = '%s %s\n' % (r1[0].rstrip(), molecular_id)
        r2[0] = '%s %s\n' % (r2[0].rstrip(), molecular_id)

        # ADAPTERTRIM
        r2[1] = '%s' % (r2[1][47:])
        r2[3] = '%s' % (r2[3][47:])
        # Chop the 5' adapter sequence from R2 
    

        for line in r1:
            r1_umitagged.write(line)
        for line in r2:
            r2_umitagged.write(line)
    r1_umitagged.close()
    r2_umitagged.close()

    # Sort fastqs based on molecular barcode
    cmd = 'cat ' + r1_umitagged_unsorted_file + ' | paste - - - - | sort -k3,3 -k1,1 | tr "\t" "\n" >' + read1_out
    subprocess.check_call(cmd, shell=True, env=os.environ.copy())
    cmd = 'cat ' + r2_umitagged_unsorted_file + ' | paste - - - - | sort -k3,3 -k1,1 | tr "\t" "\n" >' + read2_out
    subprocess.check_call(cmd, shell=True, env=os.environ.copy())


    os.remove(r1_umitagged_unsorted_file)
    os.remove(r2_umitagged_unsorted_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--read1_in', required=True)
    parser.add_argument('--read2_in', required=True)
    parser.add_argument('--read1_out', required=True)
    parser.add_argument('--read2_out', required=True)
    parser.add_argument('--out_dir', default='.')
    args = vars(parser.parse_args())
    out_dir = args['out_dir']

    umitag(args['read1_in'], args['read2_in'], args['read1_out'], args['read2_out'], args['out_dir'])
    # Because demultiplexed libraries will be run through this script, removed references to index files. Only needs R1 & R2 fastq for each sample.
    # fixed argument syntax based on reported issue.


if __name__ == '__main__':
    main()
