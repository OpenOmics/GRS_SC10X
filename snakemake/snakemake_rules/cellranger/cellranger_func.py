# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #

import os
import sys
import glob
import collections
from inspect import currentframe, getframeinfo
# ################################### INCLUDE ##################################### #
DEBUG_MODE = False
# ################################### FUNCTIONS ################################### #


def log_error(frameinfo):
	"""
	"""
	print("Error Occured at:", frameinfo.filename, frameinfo.lineno)
	sys.exit(2)
	return True

def is_path_readable(the_Path):
	"""
	"""
	if os.path.exists(the_Path) and os.access(the_Path, os.R_OK):
		#
		return True
	else:
		return False


def build_general_dict(config_Dict, wildcards):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++
	PREFIX = wildcards.prefix
	SAMPLE = wildcards.sample
	SNAKERULE = wildcards.snakerule
	INPUT_TYPE = config_Dict["INPUT_TYPE"][0]
	HOST = config_Dict["HOST"][0]
	REFERENCE = config_Dict["REFERENCE"]
	SNAKEDESIGN = PREFIX.split(SNAKERULE + "/")[1].split("/")[0]

	#SNAKEFILE = list(config_Dict["snakefile"].keys())[0]
	#SNAKERULE = PREFIX.split("/target/")[0].split("/")[-2]

	#CHEMISTRY = SNAKERULE.split("_")[1]
	# ------------------------------------
	general_Dict = {}
	# ++++++++++++++++++++++++++++++++++++
	general_Dict["SAMPLE"] = SAMPLE
	general_Dict["INPUT_TYPE"] = INPUT_TYPE
	general_Dict["SLUGIFIED_SAMPLE"] = SAMPLE.replace("-", "_")
	general_Dict["SNAKERULE"] = SNAKERULE
	general_Dict["SNAKEDESIGN"] = SNAKEDESIGN
	#general_Dict["SNAKEFILE"] = SNAKEFILE
	#general_Dict["CHEMISTRY"] = CHEMISTRY
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	general_Dict["SNAKERULE_PATH"] = PREFIX.split("target/")[0]
	
	general_Dict["SNAKERULE_REPORT_PATH"] = general_Dict["SNAKERULE_PATH"] + "report/"
	general_Dict["SNAKERULE_LOG_PATH"] = general_Dict["SNAKERULE_PATH"] + "log/"
	general_Dict["SNAKERULE_TARGET_PATH"] = general_Dict["SNAKERULE_PATH"] + "target/"
	general_Dict["SNAKERULE_TEMP_PATH"] = general_Dict["SNAKERULE_PATH"]  + "temp/"
	general_Dict["SNAKERULE_OUTPUT_PATH"] = general_Dict["SNAKERULE_PATH"] + "output/"
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	general_Dict["GENERAL_TAG"] = general_Dict["SAMPLE"] + "." + general_Dict["SNAKERULE"]
	general_Dict["TARGET_FILE"] = general_Dict["SNAKERULE_TARGET_PATH"] + general_Dict["SAMPLE"] + "." + general_Dict["SNAKERULE"] + ".target"
	general_Dict["LOG_FILE"] = general_Dict["SNAKERULE_LOG_PATH"] + general_Dict["GENERAL_TAG"] + ".log"
	general_Dict["SCRIPT_FILE"] = general_Dict["SNAKERULE_OUTPUT_PATH"] + general_Dict["GENERAL_TAG"] + ".sh"
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	general_Dict["REFERENCE"] = REFERENCE[HOST]
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	general_Dict["METADATA"] = config_Dict
	# ------------------------------------
	
	return general_Dict


def build_initialize_script(general_Dict):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++
	initialize_script_String = """#!/bin/bash
		mkdir -p {SNAKERULE_PATH}
		mkdir -p {SNAKERULE_REPORT_PATH}
		mkdir -p {SNAKERULE_LOG_PATH}
		mkdir -p {SNAKERULE_TEMP_PATH}
		mkdir -p {SNAKERULE_TARGET_PATH}
		mkdir -p {SNAKERULE_OUTPUT_PATH}
	""".format(**general_Dict)
	# ------------------------------------

	return initialize_script_String


def build_finalize_script(argument_Dict, initialize_script_String, main_execution_script_List):
	"""
	"""

	if main_execution_script_List is None:
		return ""
	finalize_script_String = ""
	finalize_script_String += initialize_script_String 
	for each_script in main_execution_script_List:
		##
		finalize_script_String += each_script
	else:
		##
		pass
	return finalize_script_String.replace("\t", "")


def build_cellranger_execution_script(config_Dict, wildcards):
	"""
	this function will invoke proper function based on snakerule
	"""
	# ++++++++++++++++++++++++++++++++++++
	
	general_Dict = build_general_dict(config_Dict, wildcards)
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	initialize_script_String = build_initialize_script(general_Dict)

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	snakerule = wildcards.snakerule
	
	# ++++++++++++++++++++++++++++++++++++
	if snakerule == "cellranger_mkfastq":
		main_execution_script_List = build_cellranger_mkfastq_script(config_Dict, general_Dict, wildcards)
	elif snakerule == "cellranger_gex":
		main_execution_script_List = build_cellranger_gex_script(config_Dict, general_Dict, wildcards)
	elif snakerule == "cellranger_vdj":
		main_execution_script_List = build_cellranger_vdj_script(config_Dict, general_Dict, wildcards)
	elif snakerule == "cellranger_atac":
		main_execution_script_List = build_cellranger_atac_script(config_Dict, general_Dict, wildcards)
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	elif snakerule == "cellranger_fbc":
		#
		main_execution_script_List = build_cellranger_fbc_script(config_Dict, general_Dict, wildcards)
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	elif snakerule == "cellranger_gex_aggr":
		main_execution_script_List = build_cellranger_gex_aggr_script(config_Dict, general_Dict, wildcards)
	elif snakerule == "cellranger_vdj_aggr":
		main_execution_script_List = build_cellranger_vdj_aggr_script(config_Dict, general_Dict, wildcards)
	elif snakerule == "cellranger_atac_aggr":
		main_execution_script_List = build_cellranger_atac_aggr_script(config_Dict, general_Dict, wildcards)
	else:
		print("can not find specifci function to build your rule", __file__)
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	finalize_script_String = build_finalize_script(general_Dict, initialize_script_String, main_execution_script_List)
	# ------------------------------------

	return (finalize_script_String, general_Dict)


def build_cellranger_mkfastq_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	# we process all wildcards into a simple dict
	
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]
	#SNAKEFILE = general_Dict["SNAKEFILE"]

	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()
	

	IO_Dict["INPUT1"] = general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"][0]
	
	sample_metadata = general_Dict["METADATA"]["sample_metadata"]
	sample_metadata_key_List = list(general_Dict["METADATA"]["sample_metadata"].keys())
	chemitsry_Dict = sample_metadata[sample_metadata_key_List[0]]
	chemistry_dict_keys = list(chemitsry_Dict.keys())
	#print(chemistry_dict_keys)
	
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"]
	
	#IO_Dict["INPUT_TYPE"] = general_Dict["INPUT_TYPE"]
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}
	if general_Dict["INPUT_TYPE"] == "bcl":
		IO_Dict["INPUT2"] = general_Dict["METADATA"]["SAMPLESHEET"][0]
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if general_Dict["INPUT_TYPE"] == "fastq":
		#
		
		if DEBUG_MODE == True:
			# ++++++++++++++++++++++++++++++++++++
			main_execution_script_String = """
				##
				#mkdir -p {OUTPUT1}{SAMPLE}
				#ln -s {INPUT1}* {OUTPUT1}{SAMPLE} \\
				>> {LOG_FILE} 2>&1
				""".format(**argument_Dict)
			# ------------------------------------
		else:
			# ++++++++++++++++++++++++++++++++++++
			main_execution_script_String = """
				##
				mkdir -p {OUTPUT1}{SAMPLE}
				ln -s {INPUT1}* {OUTPUT1}{SAMPLE} \\
				>> {LOG_FILE} 2>&1
				""".format(**argument_Dict)
			# ------------------------------------
	else:
		#
		if "atac" not in chemistry_dict_keys:
			#
			if DEBUG_MODE == True:
				# ++++++++++++++++++++++++++++++++++++
				main_execution_script_String = """
					##
					module load cellranger
					# cellranger mkfastq \\
					# 	--run={INPUT1} \\
					# 	--csv={INPUT2} \\
					# 	--localcores=16 \\
					# 	--localmem=15 \\
					#	--output-dir={OUTPUT1} \\
					>> {LOG_FILE} 2>&1
					""".format(**argument_Dict)
				# ------------------------------------
			else:
				# ++++++++++++++++++++++++++++++++++++
				main_execution_script_String = """
					##
					module load cellranger
					cellranger mkfastq \\
						--run={INPUT1} \\
						--csv={INPUT2} \\
						--localcores=16 \\
						--localmem=15 \\
						--output-dir={OUTPUT1} \\
						>> {LOG_FILE} 2>&1
					""".format(**argument_Dict)
				# ------------------------------------
		else:
			if DEBUG_MODE == True:
				# ++++++++++++++++++++++++++++++++++++
				main_execution_script_String = """
					##
					module load cellranger-atac
					# cellranger-atac mkfastq \\
					# 	--run={INPUT1} \\
					# 	--csv={INPUT2} \\
					# 	--localcores=16 \\
					# 	--localmem=15 \\
					#	--output-dir={OUTPUT1} \\
					>> {LOG_FILE} 2>&1
					""".format(**argument_Dict)
				# ------------------------------------
			else:
				# ++++++++++++++++++++++++++++++++++++
				main_execution_script_String = """
					##
					module load cellranger-atac
					cellranger-atac mkfastq \\
						--run={INPUT1} \\
						--csv={INPUT2} \\
						--localcores=16 \\
						--localmem=15 \\
						--output-dir={OUTPUT1} \\
						>> {LOG_FILE} 2>&1
					""".format(**argument_Dict)
				# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	
	return main_execution_script_List


def build_cellranger_gex_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	CHEMISTRY = SNAKERULE.split("cellranger_")[1]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]
	IO_Dict = collections.OrderedDict()
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#INPUT
	
	input_fastq_dir_List = []
	for each_input_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		
		for each_flowcell_Id in general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["Flowcell_Id"]:
			##
			input_fastq_dir_Path = each_input_target.split("target/")[0] + "output/" + each_flowcell_Id + "/"
			if is_path_readable(input_fastq_dir_Path) is False:
				#
				continue
			else:
				if DEBUG_MODE is False:
					#
					input_fastq_List = glob.glob(input_fastq_dir_Path + "*.fastq*")
					for each_fastq_file in input_fastq_List:
						##
						fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
						if SAMPLE in fastq_name:
							if input_fastq_dir_Path not in input_fastq_dir_List:
								input_fastq_dir_List.append(input_fastq_dir_Path)
							break
						else:
							pass
					else:
						#
						pass
				else:
					#if DEBUG_MODE is False:
					input_fastq_dir_List.append(input_fastq_dir_Path)
		else:
			#
			pass
	else:
		#
		pass
	
	if len(input_fastq_dir_List) == 0:
		print("no fastq files detected")
		return None
	else:
		IO_Dict["INPUT1"] = ",".join(input_fastq_dir_List)
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#REFERENCE
	if general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] == "empty":
		#
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["REFERENCE"][CHEMISTRY]
	else:
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] 
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#OUTPUT
	IO_Dict["OUTPUT1"] = general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_output"]
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger
			# cellranger count \\
			# 	--id={SAMPLE} \\
			# 	--sample={SAMPLE} \\
			# 	--fastqs={INPUT1} \\
			# 	--transcriptome={INPUT_REFERENCE1} \\
			# 	--localcores=32 \\
			# 	--localmem=40  \\
			>> {LOG_FILE} 2>&1
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger
			cellranger count \\
				--id={SAMPLE} \\
				--sample={SAMPLE} \\
				--fastqs={INPUT1} \\
				--transcriptome={INPUT_REFERENCE1} \\
				--localcores=32 \\
				--localmem=40  \\
				>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]

	return main_execution_script_List


def build_cellranger_fbc_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	CHEMISTRY = SNAKERULE.split("cellranger_")[1]
	REFERENCE = general_Dict["REFERENCE"]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]
	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()
	# ------------------------------------
	fbc_library_string_Dict = {}
	for fbc_title in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE]:
		##
		fbc_library_string_Dict[fbc_title] = "fastqs,sample,library_type\n"
		for each_fbc_sample in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][fbc_title]["snakemake_input"]["fbc"]:
			##
			input_fastq_dir_List = []
			for each_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][fbc_title]["snakemake_input"]["fbc"][each_fbc_sample]:
				##
				for each_Flowcell_Id in general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["fbc"][each_fbc_sample]['Flowcell_Id']:
					##
					input_fastq_dir_Path = each_target.split("target/")[0] + "output/" + each_Flowcell_Id + "/"
					if is_path_readable(input_fastq_dir_Path) is False:
						#
						continue
					else:
						if DEBUG_MODE is False:
							#
							input_fastq_List = glob.glob(input_fastq_dir_Path + "*.fastq*")
							for each_fastq_file in input_fastq_List:
								##
								fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
								if each_fbc_sample in fastq_name:
									if input_fastq_dir_Path not in input_fastq_dir_List:
										input_fastq_dir_List.append(input_fastq_dir_Path)
									break
								else:
									pass
							else:
								##for each_fastq_file in input_fastq_List:
								pass
						else:
							#if DEBUG_MODE is False:
							if input_fastq_dir_Path not in input_fastq_dir_List:
								input_fastq_dir_List.append(input_fastq_dir_Path)
				else:
					##
					pass
			else:
				##
				for each_fastq_path in input_fastq_dir_List:
					##
					fbc_library_string_Dict[fbc_title] += each_fastq_path + "," + each_fbc_sample + ",Antibody Capture\n"
				else:
					##
					pass
		else:
			##
			pass
		
		for each_gex_sample in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][fbc_title]["snakemake_input"]["gex"]:
			##
			input_fastq_dir_List = []
			for each_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][fbc_title]["snakemake_input"]["gex"][each_gex_sample]:
				##
				for each_Flowcell_Id in general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["gex"][each_gex_sample]['Flowcell_Id']:
					##
					input_fastq_dir_Path = each_target.split("target/")[0] + "output/" + each_Flowcell_Id + "/"
					if is_path_readable(input_fastq_dir_Path) is False:
						#
						continue
					else:
						if DEBUG_MODE is False:
							#
							input_fastq_List = glob.glob(input_fastq_dir_Path + "*.fastq*")
							for each_fastq_file in input_fastq_List:
								##
								fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
								if each_gex_sample in fastq_name:
									if input_fastq_dir_Path not in input_fastq_dir_List:
										input_fastq_dir_List.append(input_fastq_dir_Path)
									break
								else:
									pass
							else:
								##for each_fastq_file in input_fastq_List:
								pass
						else:
							#if DEBUG_MODE is False:
							if input_fastq_dir_Path not in input_fastq_dir_List:
								input_fastq_dir_List.append(input_fastq_dir_Path)
				else:
					##
					pass
			else:
				##
				for each_fastq_path in input_fastq_dir_List:
					##
					fbc_library_string_Dict[fbc_title] += each_fastq_path + "," + each_gex_sample + ",Gene Expression\n"
				else:
					##
					pass
		else:
			##
			pass
		

	else:
		##
		pass
	
	# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	general_Dict["SAMPLE"] = fbc_title
	IO_Dict["INPUT1"] = fbc_library_string_Dict[fbc_title]
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"] 
	parameters_Dict = {}
	# ---------------------------------------------------------
	
	# ++++++++++++++++++++++++++++++++++++
	#eachsample in here is the last sample being parsed
	if general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["gex"][each_gex_sample]['custom_reference'] == "empty":
		#
		
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["REFERENCE"]["gex"]
	else:
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["gex"][each_gex_sample]['custom_reference']
	
	# ------------------------------------
	
	# ++++++++++++++++++++++++++++++++++++
	
	if general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["fbc"][each_fbc_sample]['custom_reference'] == "empty":
		#
		
		IO_Dict["INPUT_REFERENCE2"] = general_Dict["REFERENCE"]["fbc_totalseq_c"]
	else:
		IO_Dict["INPUT_REFERENCE2"] = general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN]["fbc"][each_fbc_sample]['custom_reference']
	
	# ------------------------------------

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			# ##

			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------

			module load cellranger
			# cellranger count \\
			# 	--id={SAMPLE} \\
			# 	--libraries={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
			# 	--transcriptome={INPUT_REFERENCE1} \\
			# 	--feature-ref={INPUT_REFERENCE2} \\
			# 	--localcores=32 \\
			# 	--localmem=40  \\
			>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			# ##

			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------

			module load cellranger
			cellranger count \\
				--id={SAMPLE} \\
				--libraries={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
				--transcriptome={INPUT_REFERENCE1} \\
				--feature-ref={INPUT_REFERENCE2} \\
				--localcores=32 \\
				--localmem=40  \\
				>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	return main_execution_script_List



def build_cellranger_gex_aggr_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	#print(config_Dict)
	# we process all wildcards into a simple dict
	
	
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]

	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	input_aggr_file_List = []
	input_sample_List = []
	
	# log_error(getframeinfo(currentframe()))
	
	for each_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		each_sample = os.path.basename(each_target).split(".")[0]
		target_path = os.path.dirname(each_target)
		main_path = target_path.split("/target")[0]
		molecule_info_path = main_path + "/output/" + each_sample + "/outs/molecule_info.h5"
		input_sample_List.append(each_sample)
		input_aggr_file_List.append(molecule_info_path)
		
	else:
		pass
	if len(input_aggr_file_List) == 0:
		log_error(getframeinfo(currentframe()))
		return None
	else:
		#we are building the script
		cellranger_aggrs_String = "sample_id,molecule_h5\n"
		for each_sample, aggr_file in zip(input_sample_List, input_aggr_file_List):
			##
			cellranger_aggrs_String += each_sample + "," + aggr_file + "\n"
		else:
			##
			IO_Dict["INPUT1"] = cellranger_aggrs_String
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"]
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			# module load cellranger
			# cellranger aggr \\
			# 	--id={SAMPLE} \\
			# 	--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
			>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			module load cellranger
			cellranger aggr \\
				--id={SAMPLE} \\
				--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
				>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	
	return main_execution_script_List




def build_cellranger_vdj_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	CHEMISTRY = SNAKERULE.split("cellranger_")[1]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]
	IO_Dict = collections.OrderedDict()
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#INPUT
	
	input_fastq_dir_List = []
	for each_input_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		
		for each_flowcell_Id in general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["Flowcell_Id"]:
			##
			input_fastq_dir_Path = each_input_target.split("target/")[0] + "output/" + each_flowcell_Id + "/"
			if is_path_readable(input_fastq_dir_Path) is False:
				#
				continue
			else:
				if DEBUG_MODE is False:
					#
					input_fastq_List = glob.glob(input_fastq_dir_Path + "*.fastq*")
					for each_fastq_file in input_fastq_List:
						##
						fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
						if SAMPLE in fastq_name:
							if input_fastq_dir_Path not in input_fastq_dir_List:
								input_fastq_dir_List.append(input_fastq_dir_Path)
							break
						else:
							pass
					else:
						#
						pass
				else:
					#if DEBUG_MODE is False:
					input_fastq_dir_List.append(input_fastq_dir_Path)
		else:
			#
			pass
	else:
		#
		pass
	
	if len(input_fastq_dir_List) == 0:
		print("no fastq files detected")
		return None
	else:
		IO_Dict["INPUT1"] = ",".join(input_fastq_dir_List)
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#REFERENCE
	if general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] == "empty":
		#
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["REFERENCE"][CHEMISTRY]
	else:
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] 
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#OUTPUT
	IO_Dict["OUTPUT1"] = general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_output"]
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger
			# cellranger vdj \\
			# 	--id={SAMPLE} \\
			# 	--sample={SAMPLE} \\
			# 	--fastqs={INPUT1} \\
			# 	--reference={INPUT_REFERENCE1} \\
			# 	--localcores=32 \\
			# 	--localmem=40  \\
			>> {LOG_FILE} 2>&1
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger
			cellranger vdj \\
				--id={SAMPLE} \\
				--sample={SAMPLE} \\
				--fastqs={INPUT1} \\
				--reference={INPUT_REFERENCE1} \\
				--localcores=32 \\
				--localmem=40  \\
				>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]

	main_execution_script_List = [main_execution_script_String]
	return main_execution_script_List


def build_cellranger_vdj_aggr_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	#print(config_Dict)
	# we process all wildcards into a simple dict
	

	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]

	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	input_aggr_file_List = []
	input_sample_List = []
	
	frameinfo = getframeinfo(currentframe())
	print("hello I am here:", frameinfo.filename, frameinfo.lineno)
	
	for each_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		each_sample = os.path.basename(each_target).split(".")[0]
		target_path = os.path.dirname(each_target)
		main_path = target_path.split("/target")[0]
		molecule_info_path = main_path + "/output/" + each_sample + "/outs/vdj_contig_info.pb"
		input_sample_List.append(each_sample)
		input_aggr_file_List.append(molecule_info_path)
		
	else:
		pass
	
	if len(input_aggr_file_List) == 0:
		return None
	else:
		#we are building the script
		cellranger_aggrs_String = "sample_id,vdj_contig_info,donor,origin\n"
		for each_sample, aggr_file in zip(input_sample_List, input_aggr_file_List):
			##
			cellranger_aggrs_String += each_sample + "," + aggr_file + "," + each_sample + "," + each_sample + "\n"
		else:
			##
			IO_Dict["INPUT1"] = cellranger_aggrs_String
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"]
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			# module load cellranger
			# cellranger aggr \\
			# 	--id={SAMPLE} \\
			# 	--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
			>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			module load cellranger
			cellranger aggr \\
				--id={SAMPLE} \\
				--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
				>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	
	return main_execution_script_List


def build_cellranger_atac_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	CHEMISTRY = SNAKERULE.split("cellranger_")[1]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]
	IO_Dict = collections.OrderedDict()
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#INPUT
	
	input_fastq_dir_List = []
	for each_input_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		
		for each_flowcell_Id in general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["Flowcell_Id"]:
			##
			input_fastq_dir_Path = each_input_target.split("target/")[0] + "output/" + each_flowcell_Id + "/"
			if is_path_readable(input_fastq_dir_Path) is False:
				#
				continue
			else:
				if DEBUG_MODE is False:
					#
					input_fastq_List = glob.glob(input_fastq_dir_Path + "/**/*.fastq*", recursive=True)
					for each_fastq_file in input_fastq_List:
						##
						fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
						if SAMPLE in fastq_name:
							if input_fastq_dir_Path not in input_fastq_dir_List:
								input_fastq_dir_List.append(input_fastq_dir_Path)
							break
						else:
							pass
					else:
						#
						pass
				else:
					#if DEBUG_MODE is False:
					input_fastq_dir_List.append(input_fastq_dir_Path)
		else:
			#
			pass
	else:
		#
		pass
	
	if len(input_fastq_dir_List) == 0:
		print("no fastq files detected")
		return None
	else:
		IO_Dict["INPUT1"] = ",".join(input_fastq_dir_List)
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#REFERENCE
	if general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] == "empty":
		#
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["REFERENCE"][CHEMISTRY]
	else:
		IO_Dict["INPUT_REFERENCE1"] = general_Dict["METADATA"]["sample_metadata"][SNAKEDESIGN][CHEMISTRY][SAMPLE]["custom_reference"] 
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	#OUTPUT
	IO_Dict["OUTPUT1"] = general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_output"]
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger-atac
			# cellranger-atac count \\
			# 	--id={SAMPLE} \\
			# 	--sample={SAMPLE} \\
			# 	--fastqs={INPUT1} \\
			# 	--reference={INPUT_REFERENCE1} \\
			# 	--localcores=32 \\
			# 	--localmem=40  \\
			>> {LOG_FILE} 2>&1
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			module load cellranger-atac
			cellranger-atac count \\
				--id={SAMPLE} \\
				--sample={SAMPLE} \\
				--fastqs={INPUT1} \\
				--reference={INPUT_REFERENCE1} \\
				--localcores=32 \\
				--localmem=40  \\
				>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]

	return main_execution_script_List


def build_cellranger_atac_aggr_script(config_Dict, general_Dict, wildcards):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	SNAKEDESIGN = general_Dict["SNAKEDESIGN"]

	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	fragment_file_List = []
	cell_file_List = []
	input_sample_List = []
	
	# log_error(getframeinfo(currentframe()))
	
	for each_target in general_Dict["METADATA"]["snakefile"][SNAKEDESIGN][SNAKERULE][SAMPLE]["snakemake_input"]:
		##
		each_sample = os.path.basename(each_target).split(".")[0]
		target_path = os.path.dirname(each_target)
		main_path = target_path.split("/target")[0]
		fragment_path = main_path + "/output/" + each_sample + "/outs/fragments.tsv.gz"
		cell_path = main_path + "/output/" + each_sample + "/outs/singlecell.csv"
		input_sample_List.append(each_sample)
		fragment_file_List.append(fragment_path)
		cell_file_List.append(cell_path)
		
	else:
		pass
	if len(fragment_file_List) == 0:
		log_error(getframeinfo(currentframe()))
		return None
	else:
		#we are building the script
		cellranger_aggrs_String = "library_id,fragments,cells\n"
		for each_sample, fragment_file, cell_file in zip(input_sample_List, fragment_file_List, cell_file_List):
			##
			cellranger_aggrs_String += each_sample + "," + fragment_file + "," + cell_file + "\n"
		else:
			##
			IO_Dict["INPUT1"] = cellranger_aggrs_String
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"]
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			# module load cellranger-atac
			# cellranger-atac aggr \\
			# 	--id={SAMPLE} \\
			# 	--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
			>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			##
			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------
			module load cellranger-atac
			cellranger-atac aggr \\
				--id={SAMPLE} \\
				--csv={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
				>> {LOG_FILE} 2>&1 
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	
	return main_execution_script_List




def build_cellranger_fbc_script_old(config_Dict, general_Dict, wildcards):
	"""
	"""
	print("I am here now build_cellranger_fbc_script")
	#print(config_Dict)
	# we process all wildcards into a simple dict
	
	# ++++++++++++++++++++++++++++++++++++
	SAMPLE = general_Dict["SAMPLE"]
	SLUGIFIED_SAMPLE = general_Dict["SLUGIFIED_SAMPLE"]
	SNAKERULE = general_Dict["SNAKERULE"]
	
	REFERENCE = general_Dict["REFERENCE"]
	#print(config_Dict[CATEGORY][SAMPLE][RULE])
	IO_Dict = collections.OrderedDict()
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	
	sub_chemistry_Dict = {}
	for each_sub_chemistry in general_Dict["SNAKERULE_INPUT_METADATA"]["cellranger_fbc"]:
		##
		sub_chemistry_Dict[each_sub_chemistry] = {}
		
		for each_sample in general_Dict["SNAKERULE_INPUT_METADATA"]["cellranger_fbc"][each_sub_chemistry]:
			##
			sub_chemistry_Dict[each_sub_chemistry][each_sample] = {}
			sub_chemistry_Dict[each_sub_chemistry][each_sample]["reference"] = []
			sub_chemistry_Dict[each_sub_chemistry][each_sample]["fastq"] = []
			input_fastq_dir_List = []
			for each_target in general_Dict["SNAKERULE_INPUT_TARGET"]:
				##
				for each_flowcell_Id in general_Dict["SNAKERULE_INPUT_METADATA"]["cellranger_fbc"][each_sub_chemistry][each_sample]["Flowcell_Id"]:
					##
					input_fastq_dir_Path = each_target.split("target/")[0] + "output/" + each_flowcell_Id + "/"
					if is_path_readable(input_fastq_dir_Path) is False:
						#
						continue
					else:
						#
						input_fastq_List = glob.glob(input_fastq_dir_Path + "*.fastq*")
						for each_fastq_file in input_fastq_List:
							##
							fastq_name = os.path.basename(each_fastq_file).split('.fastq')[0]
							
							if each_sample in fastq_name:
								input_fastq_dir_List.append(input_fastq_dir_Path)
								break
							else:
								pass	
						else:
							##
							print(each_sample)
							print("sample not found!!")
				else:
					##
					pass
				for each_reference in general_Dict["SNAKERULE_INPUT_METADATA"]["cellranger_fbc"][each_sub_chemistry][each_sample]["custom_reference"]:
					##
					###########################################
					sub_chemistry_Dict[each_sub_chemistry][each_sample]["reference"].append(each_reference)
				else:
					pass

			else:
				##
				sub_chemistry_Dict[each_sub_chemistry][each_sample]["fastq"] = input_fastq_dir_List
		else:
			##
			pass
	else:
		## for each_sub_chemistry in general_Dict["SNAKERULE_INPUT_METADATA"]["fbc_title"]:
		pass

	print("hey I am here")
	print(sub_chemistry_Dict)
	
	if True is False:
		print("No Fastq found!!!")
		return None
	else:
		
		fbc_library_String = "fastqs,sample,library_type\n"
		for each_sub_chemistry in sub_chemistry_Dict:
			##
			for each_sample in sub_chemistry_Dict[each_sub_chemistry]:
				##
				for each_fastq in sub_chemistry_Dict[each_sub_chemistry][each_sample]["fastq"]:
					##
					if each_sub_chemistry == "gex":
						fbc_library_String += each_fastq + "," + each_sample + "," + "Gene Expression" + "\n"
					elif each_sub_chemistry == "fbc":
						#
						fbc_library_String += each_fastq + "," + each_sample + "," + "Antibody Capture" + "\n"
				else:
					##
					pass
				for each_reference in sub_chemistry_Dict[each_sub_chemistry][each_sample]["reference"]:
					##
					if each_sub_chemistry == "gex":
						#
						if each_reference == "empty":
							#
							IO_Dict["INPUT_REFERENCE1"] = REFERENCE["gex"]
						else:
							IO_Dict["INPUT_REFERENCE1"] = each_reference
					elif each_sub_chemistry == "fbc":
						#
						if each_reference == "empty":
							#
							IO_Dict["INPUT_REFERENCE2"] = REFERENCE["fbc_totalseq_c"]
						else:
							IO_Dict["INPUT_REFERENCE2"] = each_reference
					else:
						#
						pass
				else:
					##
					pass
				
			else:
				##
				pass
		else:
			##
			IO_Dict["INPUT1"] = fbc_library_String
	
	# ------------------------------------
	# # ++++++++++++++++++++++++++++++++++++
	
	# if general_Dict["SNAKERULE_INPUT_METADATA"]["custom_reference"][0] == "empty":
	# 	#
	# 	CHEMISTRY = general_Dict["SNAKERULE_INPUT_METADATA"]["Chemistry"][0].lower()
	# 	IO_Dict["INPUT_REFERENCE1"] = general_Dict["REFERENCE"][CHEMISTRY]
	# else:
	# 	IO_Dict["INPUT_REFERENCE1"] = general_Dict["SNAKERULE_INPUT_METADATA"]["custom_reference"][0]
	
	# # ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	IO_Dict["OUTPUT1"] = general_Dict["SNAKERULE_OUTPUT_PATH"]
	
	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++
	parameters_Dict = {}

	# ------------------------------------
	# ++++++++++++++++++++++++++++++++++++

	argument_Dict = {**IO_Dict, **general_Dict, **parameters_Dict}
	# ------------------------------------
	if DEBUG_MODE == True:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			# ##

			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------

			module load cellranger
			# cellranger count \\
			# 	--id={SAMPLE} \\
			# 	--libraries={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
			# 	--transcriptome={INPUT_REFERENCE1} \\
			# 	--feature-ref={INPUT_REFERENCE2} \\
			# 	--localcores=32 \\
			# 	--localmem=40  \\
			>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------
	else:
		# ++++++++++++++++++++++++++++++++++++
		main_execution_script_String = """
			# ##

			# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			echo "{INPUT1}" > {OUTPUT1}{SAMPLE}.{SNAKERULE}.csv
			# ---------------------------------------------------------

			module load cellranger
			cellranger count \\
				--id={SAMPLE} \\
				--libraries={OUTPUT1}{SAMPLE}.{SNAKERULE}.csv \\
				--transcriptome={INPUT_REFERENCE1} \\
				--feature-ref={INPUT_REFERENCE2} \\
				--localcores=32 \\
				--localmem=40  \\
				>> {LOG_FILE} 2>&1
			
			""".format(**argument_Dict)
		# ------------------------------------

	main_execution_script_List = [main_execution_script_String]
	return main_execution_script_List

# ################################### CONFIGURATION ############################### #
# ################################### WILDCARDS ################################### #
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #
# ################################### FINITO ###################################### #