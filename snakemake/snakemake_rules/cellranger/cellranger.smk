# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #

import os
import sys
from cellranger import cellranger_func
# ################################### INCLUDE ##################################### #
# ################################### FUNCTIONS ################################### #


def get_snakerule_input_target(wildcards):
	"""
	"""
	prefix = wildcards.prefix
	sample = wildcards.sample
	snakerule = wildcards.snakerule
	design = prefix.split(snakerule + "/")[1].split("/")[0]
	
	if design not in config["snakefile"]:
		return []
	if snakerule not in config["snakefile"][design]:
		return []
	
	return config["snakefile"][design][snakerule][sample]["snakemake_rule_input"]
# ################################### CONFIGURATION ############################### #
# ################################### WILDCARDS ################################### #
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #


rule cellranger:
	"""
	"""
	input:
		get_snakerule_input_target
	output:
		cellranger_output_target = "{prefix}{sample}.{snakerule}.target"
	wildcard_constraints:
		prefix = "(.+\\/)+",
		# report_path = "(.+\\/)+",
		# log_path = "(.+\\/)+",
		# sample = "((?!.*\\/).*)+",
		# suffix = "((\\.).*)+",
	params:
	resources:
	message: "Processing  {wildcards.prefix} | {wildcards.sample} | {wildcards.snakerule} "
	threads: config["main.settings"]["threads"]
	run:
		# ++++++++++++++++++++++++++++++++++++
		cellranger_execution_script, general_Dict = cellranger_func.build_cellranger_execution_script(config, wildcards)
		
		if cellranger_execution_script == "":
			print("buidling script was unsuccessful")
		else:
			shell("""
				mkdir -p $(dirname {general_Dict[SCRIPT_FILE]})
				printf "%s\\n" '{cellranger_execution_script}' 2>&1 | tee --append {general_Dict[TARGET_FILE]}.tmp {general_Dict[SCRIPT_FILE]} >/dev/null
				chmod 755 {general_Dict[SCRIPT_FILE]}
			""")
			shell("""
			cd $(dirname {general_Dict[SCRIPT_FILE]})
			
			echo "EXECUTING...."
			{general_Dict[SCRIPT_FILE]}
			
			if [ $? -eq 0 ]; then
				mv {general_Dict[TARGET_FILE]}.tmp {general_Dict[TARGET_FILE]}
				echo "DONE!!"
				
			else
				echo "FAIL!!"
				echo "Can not move temporary target to permanent target"
			fi
			""")
		# ------------------------------------

	
# ################################### FINITO ###################################### #