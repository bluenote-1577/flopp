import pysam
import sys
read_part_file = sys.argv[1]
bam_file = sys.argv[2]
pref_nam = sys.argv[3]
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

obam_files = []


for i in range(ploidy):
    obam_files.append(pysam.AlignmentFile(pref_nam+str(i)+".bam", "wb", template=bam))

for b in bam.fetch(until_eof=True):
    for i in range(ploidy):
        qnames = read_part[i]
        if b.query_name in qnames:
            obam_files[i].write(b)


for obam in obam_files:
    obam.close()
bam.close()
