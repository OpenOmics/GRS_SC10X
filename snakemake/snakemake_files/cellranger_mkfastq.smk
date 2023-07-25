# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #

import os
import sys
library_path = os.path.abspath(workflow.basedir + "/../library/")
snakemake_rules_path = os.path.abspath(workflow.basedir + "/../snakemake_rules")
sys.path.append(library_path)
sys.path.append(snakemake_rules_path)
import utility
# ################################### INCLUDE ##################################### #

include: snakemake_rules_path + "/general/main.settings.smk"
include: snakemake_rules_path + "/general/files.settings.smk"
include: snakemake_rules_path + "/cellranger/cellranger.settings.smk"
# ################################### FUNCTIONS ################################### #
# ++++++++++++++++++++++++++++++++++++
sample_Dict = {}
sample_Dict["sample_metadata"] = utility.build_sample_metadata_dict(config)

cellranger_mkfastq_IO_Dict = utility.build_cellranger_mkfastq_IO_dict(config, sample_Dict["sample_metadata"])
# ------------------------------------
# ################################### CONFIGURATION ############################### #
# ################################### WILDCARDS ################################### #
# ++++++++++++++++++++++++++++++++++++
update_config(sample_Dict, config)
config = sample_Dict


update_config(cellranger_mkfastq_IO_Dict, config)
config = cellranger_mkfastq_IO_Dict
# ------------------------------------

# ################################### PIPELINE FLOW ############################### #
rule End_Point:
	input:
		cellranger_mkfastq_IO_Dict["snakefile"]["snakefile_target_List"]
# ################################### PIPELINE RULES ############################## #

include: snakemake_rules_path + "/cellranger/cellranger.smk"
# ################################### FINITO ###################################### #
