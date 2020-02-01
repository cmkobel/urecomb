from gwf import *



goodbye = "echo JOBID $SLURM_JOBID; jobinfo $SLURM_JOBID"



def smalt_index(target_dir, group, reference_stem):

	inputs = 'reference_genomes/' + reference_stem + '.fasta'
	outputs = ['reference_genomes/' + reference_stem + '.smi',
	           'reference_genomes/' + reference_stem + '.sma']
	options = {'nodes': 1, 'cores': 1, 'memory': '8g', 'walltime': '1:00:00',  'account': 'clinicalmicrobio'}
	spec = f"""

# mkdir {target_dir}/group
# cd {target_dir}/group

cd reference_genomes/

smalt index -k 14 -s 8 {reference_stem} {reference_stem}.fasta


{goodbye}
	"""
	return inputs, outputs, options, spec



def smalt_map(group, sample, forward, reverse, reference_stem):
	inputs = ['reference_genomes/' + reference_stem + '.smi',
	           'reference_genomes/' + reference_stem + '.sma']
	outputs = ['output/' + group + '/' + sample + '.sorted.bam']
	options = {'nodes': 1, 'cores': 4, 'memory': '16g', 'walltime': '2:00:00',  'account': 'clinicalmicrobio'}
	spec = f"""

mkdir -p output/{group}
cd output/{group}


smalt map -n 4 ../../reference_genomes/{reference_stem} ../../{forward} ../../{reverse} | \
samtools sort -t tmp > {sample}.sorted.bam


{goodbye}
	"""
	return inputs, outputs, options, spec



def mcorr_bam_fit(group, sample, forward, reverse, reference_stem):
	inputs = ['output/' + group + '/' + sample + '.sorted.bam']
	outputs = ['output/' + group + '/' + sample + '.csv',  # mcorr_bam
	           'output/' + group + '/' + sample + '.json', # mcorr_bam
	           'output/' + group + '/' + sample + '_best_fit.svg',  # mcorr_fit
	           'output/' + group + '/' + sample + '_fit_reports.txt',  # mcorr_fit
	           'output/' + group + '/' + sample + '_fit_results.csv']  # mcorr_fit
	           #'output/' + group + '/' + sample + '_parameter_histograms.svg']  # mcorr_fit
	options = {'nodes': 1, 'cores': 4, 'memory': '24g', 'walltime': '2:00:00',  'account': 'clinicalmicrobio'}
	spec = f"""
mkdir -p output/{group}
cd output/{group}

mcorr-bam ../../reference_genomes/{reference_stem}.gff3 {sample}.sorted.bam {sample}

mcorr-fit {sample}.csv {sample}


{goodbye}
"""
	return inputs, outputs, options, spec