#Author Carl


import pandas as pd
from gwf import *
from workflow_templates import *


def sanify(input):
    """ Makes sure that the name of the gwf target is not illegal. """
    output = []
    
    for i in str(input):
        
        ascii = ord(i)
        if (ascii >= 48 and ascii <= 57) or (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122) or ascii == 95:
            output.append(i)
        else:
            output.append('_')

    return ''.join(output)


gwf = Workflow(defaults={
    "mail_user": "kobel@pm.me",
    "mail_type": "FAIL",
})

target_dir = '/faststorage/project/ClinicalMicrobio/10carl/urecomb/workflow/output'



### I: Reference genomes and their indexing ###
reference_genomes = {'TG_mitis': 'mitis_b6'}
                      #'Aactinomycetemcomitans': 'path'}
for group, reference_stem in reference_genomes.items(): # index all genomes
	print(group, reference_stem)

	gwf.target_from_template(sanify('ure_smaltindex_' + group), smalt_index(target_dir, group, reference_stem))




### II: For each sample in the data set ###
input_data = pd.read_csv('input.tab', delimiter = '\t')
print(input_data.columns)

for sample_, sample in input_data.iterrows():

	pass
	




### III: For each group ###