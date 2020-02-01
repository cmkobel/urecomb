from gwf import *



def smalt_index(target_dir, group, reference_stem):

	inputs = 'reference_genomes/' + reference_stem + '.fasta'
	outputs = ['reference_genomes/index/' + reference_stem + '.smi',
	           'reference_genomes/index/' + reference_stem + '.sma']
	options = {'nodes': 1, 'cores': 1, 'memory': '8g', 'walltime': '1:00:00',  'account': 'clinicalmicrobio'}
	spec = f"""

# mkdir {target_dir}/group
# cd {target_dir}/group

cd reference_genomes/index/

smalt index -k 14 -s 8 {reference_stem} ../{reference_stem}.fasta

"""

	return inputs, outputs, options, spec