from gwf import *



goodbye = "echo JOBID $SLURM_JOBID; jobinfo $SLURM_JOBID"



def smalt_index(target_dir, group, reference_stem):

    inputs = 'reference_genomes/' + reference_stem + '.fasta'
    outputs = ['reference_genomes/' + reference_stem + '.smi',
               'reference_genomes/' + reference_stem + '.sma',
               'reference_genomes/' + reference_stem + '.gene.txt']
    options = {'nodes': 1, 'cores': 1, 'memory': '8g', 'walltime': '1:00:00',  'account': 'clinicalmicrobio'}
    
    spec = f"""

# mkdir {target_dir}/group
# cd {target_dir}/group

cd reference_genomes/

smalt index -k 14 -s 8 {reference_stem} {reference_stem}.fasta

# Later, when we are going to extract the gene sequences from each isolate, we are only interested in the genes.
cat {reference_stem}.gff3 | awk '$3 == "gene" {{print}}' > {reference_stem}.gene.txt




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
samtools sort > {sample}.sorted.bam



{goodbye}
    """
    return inputs, outputs, options, spec




def consensus(group, sample, reference_stem):
    inputs = ['output/' + group + '/' + sample + '.sorted.bam']
    outputs = ['output/' + group + '/' + sample + '.fasta']
    options = {'nodes': 1, 'cores': 4, 'memory': '16g', 'walltime': '2:00:00',  'account': 'clinicalmicrobio'}
    spec = f"""

mkdir -p output/{group}
cd output/{group}


samtools mpileup -f ../../reference_genomes/{reference_stem}.fasta {sample}.sorted.bam | \
GenomicConsensus --fna_file ../../reference_genomes/{reference_stem}.fasta > {sample}.fasta 


{goodbye}
    """
    return inputs, outputs, options, spec



def mcorr_bam_fit(group, sample, forward, reverse, reference_stem):
    inputs = ['reference_genomes/' + reference_stem + '.gff3',
              'output/' + group + '/' + sample + '.sorted.bam']
    outputs = ['output/' + group + '/' + sample + '.csv',  # mcorr_bam
               'output/' + group + '/' + sample + '.json', # mcorr_bam
               'output/' + group + '/' + sample + '_best_fit.svg',  # mcorr_fit
               'output/' + group + '/' + sample + '_fit_reports.txt',  # mcorr_fit
               'output/' + group + '/' + sample + '_fit_results.csv']  # mcorr_fit
               #'output/' + group + '/' + sample + '_parameter_histograms.svg']  # mcorr_fit # fejl muligvis relateret til -t -T i samtools sort
    options = {'nodes': 1, 'cores': 4, 'memory': '64g', 'walltime': '2:00:00',  'account': 'clinicalmicrobio'}
    spec = f"""
mkdir -p output/{group}
cd output/{group}

mcorr-bam ../../reference_genomes/{reference_stem}.gff3 {sample}.sorted.bam {sample}

mcorr-fit {sample}.csv {sample} || echo "probably not enough memory"



{goodbye}
"""
    return inputs, outputs, options, spec




def extract_fasta_from_bed(group, sample, reference_stem):
    inputs = [#'output/' + group + '/' + sample + '.sorted.bam',
              'output/' + group + '/' + sample + '.fasta',
              'reference_genomes/' + reference_stem + '.gff3']
    outputs = ['output/' + group + '/' + sample + '.extracted.fasta']
               #'output/' + group + '/' + sample + '_parameter_histograms.svg']  # mcorr_fit # fejl muligvis relateret til -t -T i samtools sort
    options = {'nodes': 1, 'cores': 4, 'memory': '8g', 'walltime': '2:00:00',  'account': 'clinicalmicrobio'}
    spec = f"""
mkdir -p output/{group}
cd output/{group}

# The index is automatically generated
bedtools getfasta -fi {sample}.fasta -bed ../../reference_genomes/{reference_stem}.gene.gff3 > {sample}.extracted.fasta




{goodbye}
"""
    return inputs, outputs, options, spec



