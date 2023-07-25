# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #
# ################################### INCLUDE ##################################### #
# ################################### FUNCTIONS ################################### #
# ################################### CONFIGURATION ############################### #


config_default = {
	"files_metadata": {
		"supported_format_file_list": ["fastq", "fasta"],
		"fastq":{
			"format": "fastq",
			"delimiter": "",
			"layout_List": ["paired", "single"],
			"extension_List": [".fastq.gz", ".fq.gz", ".fastq", ".fq"],
			"extension_regex": "(\.fastq\.gz$|\.fq\.gz$|\.fastq$|\.fq$)",
			"forward_name_tag_List": ["_1", "_R1", ".1", ".R1"],
			"reverse_name_tag_List": ["_2", "_R2", ".2", ".R2"],
			"forward_name_tag_regex": "(_1|_R1|\.1|\.R1)",
			"reverse_name_tag_regex": "(_2|_R2|\.2|\.R2)",
		},
		"fasta":{
			"format": "fasta",
			"delimiter": "",
			"layout_List": ["paired", "single"],
			"extension_List": [".fasta.gz", ".fa.gz", ".fasta", ".fa"],
			"extension_regex": "(\.fasta\.gz$|\.fa\.gz$|\.fasta$|\.fa$)",
			"forward_name_tag_List": ["_1", "_R1", ".1", ".R1"],
			"reverse_name_tag_List": ["_2", "_R2", ".2", ".R2"],
			"forward_name_tag_regex": "(_1|_R1|\.1|\.R1)",
			"reverse_name_tag_regex": "(_2|_R2|\.2|\.R2)"
		},
		"bigwig":{
			"format": "bigwig",
			"delimiter": "",
			"layout": ["paired", "single"],
			"extension": [".bigwig", ".bw"],
			"extension_regex": "(\.bigwig$|\.bw$)",
		},
		"bam":{
			"format": "bam",
			"delimiter": "",
			"layout_List": ["paired", "single"],
			"extension_List": [".bam", ".sam"]
		},
		"rsem_genes": {
			"format": "txt",
			"delimiter": "tab",
			"index_column": "gene_id",
			"columns_List": ["gene_id", "transcript_id(s)", "length", "effective_length", "expected_count", "TPM", "FPKM"]
		},
		"rsem_isoforms": {
			"format": "txt",
			"delimiter": "tab",
			"index_column": "gene_id",
			"columns_List": ["gene_id", "transcript_id(s)", "length", "effective_length", "expected_count", "TPM", "FPKM"]
		},
		"feature_counts":{
			"format": "txt",
			"delimiter": "tab",
			"index_column": "ensembl_gene_id",
			"columns_List": ["ensembl_gene_id", "hgnc_symbol", "entrezgene_description"]
		},
		"png":{
			"format": "png"
		}
	}
}
update_config(config_default, config)
config = config_default
# ################################### WILDCARDS ################################### #
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #
# ################################### FINITO ###################################### #