import pysam
import subprocess
import sys

if len(sys.argv) < 4:
    print("usage: haplotag_bam.py contig_part.txt original_bam.bam new_haplotagged_bam_name.bam")
    exit()

read_part_file = sys.argv[1]
bam_file = sys.argv[2]
new_name = sys.argv[3]
bam = pysam.AlignmentFile(bam_file)

read_part = []

count_i = -1 
for line in open(read_part_file,'r'):
    if '#' in line:
        read_part.append(set())
        count_i += 1
    else:
        read_part[count_i].add(line.split()[0])

ploidy = len(read_part)

new_bam_name = new_name
new_bam_file = pysam.AlignmentFile(new_bam_name, "wb", template=bam)

for b in bam.fetch(until_eof=True):
    not_frag = True;
    for i in range(ploidy):
        qnames = read_part[i]
        if b.query_name in qnames:
            b.set_tag('HP',i,value_type='i')
            new_bam_file.write(b)
            not_frag=False
    if not_frag:
            new_bam_file.write(b)

bam.close()
