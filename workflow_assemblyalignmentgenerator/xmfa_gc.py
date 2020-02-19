#!/usr/bin/env python

""" 
    This file takes all the genes from an single-line formatted .xmfa-file and calculates
    the mean GC content. The output is printed to STDOUT
"""

import sys, json

#Warning! This script only works for single line sequences

input_file = sys.argv[1]


dict = {}

with open(input_file, 'r') as file:
    for line in file:
        line_s = line.strip()
        if line_s == "=":
            #print('skipping')
            del gene, isolate, dna
            continue
        elif line_s[0] == ">":

            gene, isolate = line_s[1:].split("|")
        

            #print(gene, isolate)

            # calculate GC content of DNA string
            
            dna = next(file)
            #print(dna[:60])

            dna_gc = 0.0
            for i in dna:
                if i.upper() in "GC":
                    dna_gc += 1

            gc_content = dna_gc / float(len(dna))

            if gene in dict:
                dict[gene].append(gc_content)
            else:
                dict[gene] = [gc_content]


#print(json.dumps(dict, indent = 4))


# Calculate means for each gene.

for key, value in dict.items():
    print(key, sum(value)/len(value), sep = '\t')


            
        
            
        

