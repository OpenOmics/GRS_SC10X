# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #
# ################################### INCLUDE ##################################### #
# ################################### FUNCTIONS ################################### #
# ################################### CONFIGURATION ############################### #

config_default = {
	"cellranger_mkfastq_setting":{
		"cmd": "cellranger mkfastq",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_mkfastq.sh",
		"tag": ".cellranger_mkfastq",
		"message": "running cellranger mkfastq: ",
		"target": ".cellranger_mkfastq.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},
	"cellranger_gex_setting":{
		"cmd": "cellranger count",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_gex.sh",
		"tag": ".cellranger_gex",
		"message": "running cellranger count: ",
		"target": ".cellranger_gex.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},
	
	"cellranger_vdj_setting":{
		"cmd": "cellranger vdj",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_vdj.sh",
		"tag": ".cellranger_vdj",
		"message": "running cellranger vdj: ",
		"target": ".cellranger_vdj.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_atac_setting":{
		"cmd": "cellranger atac",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_atac.sh",
		"tag": ".cellranger_atac",
		"message": "running cellranger atac: ",
		"target": ".cellranger_atac.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_fbc_setting":{
		"cmd": "cellranger fbc",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_fbc.sh",
		"tag": ".cellranger_fbc",
		"message": "running cellranger fbc: ",
		"target": ".cellranger_fbc.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_arc_setting":{
		"cmd": "cellranger fbc",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_fbc.sh",
		"tag": ".cellranger_fbc",
		"message": "running cellranger fbc: ",
		"target": ".cellranger_fbc.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_gex_aggr_setting":{
		"cmd": "cellranger aggr",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_gex_aggr.sh",
		"tag": ".cellranger_gex_aggr",
		"message": "running cellranger_gex_aggr: ",
		"target": ".cellranger_gex_aggr.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_vdj_aggr_setting":{
		"cmd": "cellranger aggr",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_vdj_aggr.sh",
		"tag": ".cellranger_vdj_aggr",
		"message": "running cellranger_vdj_aggr: ",
		"target": ".cellranger_vdj_aggr.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_atac_aggr_setting":{
		"cmd": "cellranger atac",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_atac_aggr.sh",
		"tag": ".cellranger_atac_aggr",
		"message": "running cellranger_atac_aggr: ",
		"target": ".cellranger_atac_aggr.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},

	"cellranger_fbc_aggr_setting":{
		"cmd": "cellranger fbc",
		"conda": "cellranger",
		"extra_prefix": "",
		"script": "cellranger_fbc_aggr.sh",
		"tag": ".cellranger_fbc_aggr",
		"message": "running cellranger_fbc_aggr: ",
		"target": ".cellranger_fbc_aggr.target",
		"options": "",
		"input_pattern": {
		},
		"output_pattern": {
		}

	},
	


}
# ################################### WILDCARDS ################################### #
# ++++++++++++++++++++++++++++++++++++
update_config(config_default, config)
config = config_default
# ------------------------------------
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #
# ################################### FINITO ###################################### #