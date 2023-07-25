# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #


from multiprocessing import cpu_count
# ################################### INCLUDE ##################################### #
# ################################### FUNCTIONS ################################### #
# ################################### CONFIGURATION ############################### #

# ++++++++++++++++++++++++++++++++++++
# CLUSTER PRAMETERS
PROCESSORS = max(2, cpu_count() - 2)
# ------------------------------------

config_default = {
	"main.settings": {
		"threads": PROCESSORS,
		"init_conda": "set +eu && PS1=dummy && . /data/$USER/conda/etc/profile.d/conda.sh;"
	}
}

update_config(config_default, config)
config = config_default
# ################################### WILDCARDS ################################### #
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #
# ################################### FINITO ###################################### #