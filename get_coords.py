#!/usr/bin/env python

import argparse

#command line arguments
parser=argparse.ArgumentParser()
parser.add_argument('-fa', type=str, help='contig fasta')
parser.add_argument('-coords', type=str, help='coordintes to extract')
parser.add_argument('-out', type=str, help='name for output file')
args=parser.parse_args()
(fasta, coords, outfile)=(args.fa, args.coords, args.out)

#create file handles
fasta_fh=open(fasta, "r")
coords_fh=open(coords, "r")
out_fh=open(outfile, "w")

#make dictonary out of fasta file, with contig name as key, and sequence string as value
fasta_dict={}
line_1=True
for line in fasta_fh:
	line=line.strip()
	if line.startswith(">") and line_1==True: #no previous sequence to store in dict
		contig=line[1:]
		sequence=""
		line_1=False
		continue
	elif line.startswith(">"): #store previous sequence and contig in dictionary, reinitiaize variables
		fasta_dict[contig]=sequence
		contig=line[1:]
		sequence=""
		continue
	elif len(sequence)==0: #previous line was the descriptor, thus sequence string is empty 
		sequence=line
		continue
	else: #concatenate lines of the same sequence together
		sequence=sequence+line	

else: #this block will add the last sequence from the file into the dictioanry; necessary for the way that the conditionals are constructed
	fasta_dict[contig]=sequence
fasta_fh.close()


#function for extracting sequence 
#coords_list refers to a line in the coordinate file, ex: 1:4235-6522
#fasta_dict refers to the dictionary containing the fasta sequences
def extract_sequence(coords_line, fasta_dict): 
	coords=coords_line.split(":")
	contig=coords[0]
	seq_range=coords[1].split("-")
	first=int(seq_range[0])-1
	second=int(seq_range[1])
	sequence=fasta_dict[contig][first:second]
	return contig, seq_range[0], seq_range[1], sequence

for line in coords_fh:
	line=line.strip()
	sequence=extract_sequence(line, fasta_dict)
	out_fh.write(">"+sequence[0]+":"+sequence[1]+"-"+sequence[2]+"\n"+sequence[3]+"\n")
