# ################################### INFO ###################################### #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ##################################### #

import os
import sys
import pandas
import numpy
import json
import collections
import traceback
import xml.etree.ElementTree as ET
from copy import copy
import glob
# ################################### FUNCTIONS ################################## #


def is_file_exist(file_Path):
	"""
	"""
	if os.path.isfile(file_Path) and os.path.exists(file_Path) and os.access(file_Path, os.R_OK):
		return True
	else:
		return False


def is_path_readable(the_Path):
	"""
	"""
	if os.path.exists(the_Path) and os.access(the_Path, os.R_OK):
		#
		return True
	else:
		return False


def is_path_writeable(the_Path):
	"""
	"""
	if os.path.exists(the_Path) and os.access(the_Path, os.W_OK):
		#
		return True
	else:
		return False


def is_dataframe_empty(samplesheet_DF):
	"""
	"""
	if samplesheet_DF.empty is True or len(samplesheet_DF.index) == 0:
		#
		return True
	else:
		return False

def fix_file_path(file_path):
	"""
	"""
	if file_path[:-1] != "/":
		fixed_path = file_path + "/"
	else:
		pass
	return fixed_path


def parse_metadata_dict(metadata_DF):
	"""
	"""
	
	transposed_metadata_Dict = metadata_DF.fillna('empty').T.to_dict('list')
	#print(transposed_metadata_Dict["input"][0][1:-1].split(","))
	transposed_metadata_Dict["input"] = transposed_metadata_Dict["input"][0].split(";")
	
	return transposed_metadata_Dict


def convert_xml_to_dict(r,root=True):
	if root:
		return {r.tag : convert_xml_to_dict(r, False)}
	d=copy(r.attrib)
	if r.text:
		d["_text"]=r.text
	for x in r.findall("./*"):
		if x.tag not in d:
			d[x.tag]=[]
		d[x.tag].append(convert_xml_to_dict(x,False))
	return d
	

def validate_bcl_dir(bcl_directory_Path):
	"""
	"""
	#step1 check if bcl file completed

	RunCompletionStatus_File_Path = os.path.join(bcl_directory_Path, "RunCompletionStatus.xml")
	
	if is_file_exist(RunCompletionStatus_File_Path) is False:
		#NextSeq500
		print("bcl file vaidation failed.")
		print("please make sure the input directory contains all bcl files and directories")
		print("Aborting!!")
		sys.exit(2)
	else:
		pass
	tree = ET.parse(os.path.join(bcl_directory_Path, "RunCompletionStatus.xml"))
	root = tree.getroot()
	RunCompletionStatus_Dict = convert_xml_to_dict(root)
	if 'RunCompletionStatus' in RunCompletionStatus_Dict:
		#NextSeq2000
		if 'CompletionStatus' in RunCompletionStatus_Dict['RunCompletionStatus']:
			CompletionStatus_Value = RunCompletionStatus_Dict['RunCompletionStatus']['CompletionStatus'][0]['_text']
			print(CompletionStatus_Value)
		else:
			print("bcl file vaidation failed.")
			print("please make sure the input directory contains all bcl files and directories")
			print("Aborting!!")
			sys.exit(2)
	elif 'SequenceRunCompletionStatus' in RunCompletionStatus_Dict:
		#
		if 'RunStatus' in RunCompletionStatus_Dict['SequenceRunCompletionStatus']:
			CompletionStatus_Value = RunCompletionStatus_Dict['SequenceRunCompletionStatus']['RunStatus'][0]['_text']
			print(CompletionStatus_Value)
		else:
			print("bcl file vaidation failed.")
			print("please make sure the input directory contains all bcl files and directories")
			print("Aborting!!")
			sys.exit(2)
	
	return True


def validate_fastq_dir(fastq_input_directory_List, sample_sheet_Dict):
	"""
	we make sure all sample exist
	"""
	fastq_sample_List = []
	for each_fastq_dir in fastq_input_directory_List:
		##
		#step1 check if fastq files exist and it is 4 per sample
		fastq_List = glob.glob(each_fastq_dir + "/**/*.fastq.gz", 	recursive=True)
		if len(fastq_List) == 0:
			#
			print("no fastq file detected")
			print("please make sure the input directory contains fastq files")
			print("Input Directory: ", each_fastq_dir)
			print("Aborting!!")
			sys.exit(2)
		else:
			for each_fastq in fastq_List:
				##
				fastq_sample_List.append(os.path.basename(each_fastq))
			else:
				##
				pass
	else:
		##
		pass
	for each_sample in sample_sheet_Dict["Sample"]:
		#
		sample_flag = False
		for each_fastq in fastq_sample_List:
			if each_sample in each_fastq:
				#
				sample_flag = True
				break
			else:
				pass
		else:
			if sample_flag is False:
				#
				print("samples in design missing from provided input list")
				print("please make sure your samples in design file avaiable in input directry")
				print("missing sample: ", each_sample)
				print("Aborting")
				sys.exit(2)
			else:
				pass
		
	else:
		pass

	return True


def parse_csv_to_dict(csv_file_Path):
	"""
	"""
	sample_sheet_DF = pandas.read_csv(
		csv_file_Path,
		encoding=None,
		skip_blank_lines=True,
		delimiter=",",
		index_col=None,
		#header=None
	)
	if is_dataframe_empty(sample_sheet_DF) is True:
		#
		print("csv file is empty!!")
		print("csv file_path:", csv_file_Path)
		print("ABORTING!!!")
		sys.exit(2)
	##
	transposed_sample_sheet_Dict = sample_sheet_DF.fillna('empty').to_dict('list')
	return transposed_sample_sheet_Dict



def validate_design(metadata_Dict):
	"""
	#step1: check it is not empty file
	#step2: check if it is standard format
	#step3: check if custom reference exist and available
	#step4: check chemistry is valid
	"""
	design_file_Path = metadata_Dict["design"][0]
	#step1
	design_Dict = parse_csv_to_dict(design_file_Path)
	# print(design_Dict)
	#step2
	
	design_column_List = ["Sample", "Design", "Index", "Chemistry", "custom_reference"]
	if all(name in design_Dict for name in design_column_List) is False:
		#
		print("design file is not standard!!")
		print("please make sure that these column is available, case sensitive!!")
		print(design_column_List)
		print("design file_path:", design_file_Path)
		print("ABORTING!!!")
		sys.exit(2)
	else:
		#if all(name in design_Dict for name in design_column_List) is False:
		pass
	#step3
	for each_reference in design_Dict["custom_reference"]:
		##
		if each_reference == "empty":
			#
			continue
		else:
			#
			if is_file_exist(each_reference) is False:
				#
				print("provided custom reference file is not accessible; it is either not available or premission")
				print("custom_reference: {}".format(each_reference))
				print("ABORTING!!!")
				sys.exit(2)
			elif is_path_readable(each_reference) is False:
				#
				print("provided custom reference file is not readable")
				print("custom_reference: {}".format(each_reference))
				print("ABORTING!!!")
				sys.exit(2)
			else:
				reference_Dict = parse_csv_to_dict(each_reference)
				reference_column_List = ["id", "name", "feature_type", "read", "pattern", "sequence"]
				if all(name in reference_Dict for name in reference_column_List) is False:
					#
					print("custom reference file is not standard!!")
					print("please make sure that these column is available, case sensitive!!")
					print(reference_column_List)
					print("reference file_path:", each_reference)
					print("ABORTING!!!")
					sys.exit(2)
				else:
					#if all(name in reference_Dict for name in reference_column_List) is False:
					pass


	else:
		##for each_reference in design_Dict["custom_reference"]:
		pass
	#step4
	standard_chemistry_List = ["vdj", "gex", "atac", "fbc"]
	chemistry_List = design_Dict["Chemistry"]
	for each_chemistry in chemistry_List:
		##
		if each_chemistry.lower() not in standard_chemistry_List:
			print("unsupported chemistry!!")
			print("we support " + ",".join(standard_chemistry_List))
			print("ABORTING!!")
			sys.exit(2)
		else:
			pass
	else:
		##
		pass
	
	return design_Dict


def validate_sample_sheet(metadata_Dict):
	"""
	#step1: check it is not empty file
	#step2: check if it is standard format
	"""
	sample_sheet_file_Path = metadata_Dict["sample-sheet"][0]
	#step1
	sample_sheet_Dict = parse_csv_to_dict(sample_sheet_file_Path)
	#step2
	sample_sheet_column_List = ["Lane", "Sample", "Index"]
	if all(name in sample_sheet_Dict for name in sample_sheet_column_List) is False:
		#
		print("sample sheet file is not standard!!")
		print("please make sure that these column is available, case sensitive!!")
		print(sample_sheet_column_List)
		print("sample sheet file_path:", sample_sheet_file_Path)
		print("ABORTING!!!")
		sys.exit(2)
	else:
		#if all(name in sample_sheet_column_List for name in sample_sheet_Dict) is False:
		pass
	
	return sample_sheet_Dict


def verify_design_sample_sheet(sample_sheet_Dict, design_Dict):
	"""
	"""
	
	if set(sample_sheet_Dict["Sample"]) != set(design_Dict["Sample"]):
		#
		print("sample_sheet Samples not matches with design Samples")
		print("ABORTING!!!")
		sys.exit(2)
	
	elif set(sample_sheet_Dict["Index"]) != set(design_Dict["Index"]):
		#
		print("sample_sheet Samples not matches with design Samples")
		print("ABORTING!!!")
		sys.exit(2)
	return True


def validate_metadata(metadata_Dict):
	"""
	validate sample_sheet
	validate design
	validate input
	"""
	
	input_type  = metadata_Dict["input-type"][0]
	design_Dict = validate_design(metadata_Dict)
	if metadata_Dict["sample-sheet"][0] != "empty":
		#
		sample_sheet_file_Path = metadata_Dict["sample-sheet"][0]
		sample_sheet_Dict = validate_sample_sheet(metadata_Dict)
		verify_design_sample_sheet(sample_sheet_Dict, design_Dict)
	else:
		#
		pass
	
	
	if metadata_Dict["input-type"][0] == "bcl":
		#
		for each_directory in metadata_Dict["input"]:
			##
			validate_bcl_dir(each_directory)
		else:
			##
			pass
	elif metadata_Dict["input-type"][0] == "fastq":
		# a method to make sure fastq files is available
		validate_fastq_dir(metadata_Dict["input"], design_Dict)
		
	else:
		pass



	return True


def process_metadata(metadata_file_Path):
	"""
	"""
	metadata_DF = pandas.read_csv(
		metadata_file_Path,
		encoding=None,
		skip_blank_lines=True,
		delimiter=",",
		index_col=0,
		header=None
	)
	
	#step1: check if it empty or not
	if is_dataframe_empty(metadata_DF) is True:
		#
		print("metadata file is empty!!")
		print("metadata_file_path:", metadata_file_Path)
		print("check the: ", os.path.basename(__file__))
		print("ABORTING!!!")
		sys.exit(2)
	else:
		pass
	#step2 parse it into dict
	metadata_Dict =  parse_metadata_dict(metadata_DF)
	
	#step3 validate
	validate_metadata(metadata_Dict)
	#step 4 fix input path
	input_path_List = []
	for each_input in metadata_Dict["input"]:
		input_path_List.append(fix_file_path(each_input))
	else:
		pass
	metadata_Dict["input"] = input_path_List

	#step4 remove list like 
	processed_metadata_Dict = {}
	processed_metadata_Dict["TITLE"] = metadata_Dict["title"]
	processed_metadata_Dict["HOST"] = metadata_Dict["host"]
	processed_metadata_Dict["INPUT_TYPE"] = metadata_Dict["input-type"]
	if metadata_Dict["sample-sheet"][0] != "empty":
		#
		processed_metadata_Dict["SAMPLESHEET"] = metadata_Dict["sample-sheet"]
	else:
		#
		pass
	processed_metadata_Dict["INPUT"] = metadata_Dict["input"]
	processed_metadata_Dict["OUTPUT"] = metadata_Dict["output"]
	processed_metadata_Dict["DESIGN"] = metadata_Dict["design"]
	processed_metadata_Dict["MODE"] = metadata_Dict["mode"]
	return processed_metadata_Dict


def process_reference(execution_directory_Path):
	"""
	"""
	
	reference_file_Path = execution_directory_Path + "/../template/GRS_SC10X_reference_metadata.csv"
	
	if is_file_exist(reference_file_Path) is False:
		#
		print("reference file is missing, please check template directory")
		print("ABORTING!!!")
		sys.exit(2)
	else:
		#
		pass
	reference_sheet_DF = pandas.read_csv(
		reference_file_Path,
		encoding=None,
		skip_blank_lines=True,
		delimiter=",",
		index_col="host"
	)
	#
	if is_dataframe_empty(reference_sheet_DF) is True:
		#dataframe is empty
		print("FATAL ERROR: reference_sheet is empty!!!\nReference_sheet file Path: " + reference_file_Path + "\n")
		raise Exception("ABORTING!!!")
		sys.exit(2)
	else:
		#
		pass
	#
	reference_sheet_DF.replace(numpy.nan, '', regex=True)
		
	#
	transposed_reference_sheet_DF = reference_sheet_DF.transpose()
	reference_sheet_Dict = transposed_reference_sheet_DF.to_dict()
	return reference_sheet_Dict

	

def build_execution_metadata(processed_metadata_Dict, processed_reference_Dict, execution_json_file_Path):
	"""
	"""
	execution_dict = processed_metadata_Dict
	execution_dict["REFERENCE"] = processed_reference_Dict

	execution_Json = json.dumps(execution_dict, indent=4)


	with open(execution_json_file_Path, "w") as metadata_json:
		metadata_json.write(execution_Json)
	return True


def build_execution_bash(metadata_Dict, execution_json_file_Path, execution_bash_file_Path):
	"""
	"""

	GRS_SC10X_directory = os.path.dirname(__file__) + "/.." 

	cellranger_mkfastq_cluster_config_script = """--cluster="sbatch --cpus-per-task={core} --mem={memory} --partition={partition} --time={time} --mail-type=ALL --job-name={jobname} --output={workdir}/snakemake_log/cellranger_mkfastq/{output} --error={workdir}/snakemake_log/cellranger_mkfastq/{error} {extra}" """.format(
		workdir=metadata_Dict["OUTPUT"][0] + "/" + metadata_Dict["TITLE"][0],
		core="{cluster.core}",
		memory="{cluster.memory}",
		partition = "{cluster.partition}",
		time="{cluster.time}",
		jobname="{cluster.jobname}",
		output="{cluster.output}",
		error="{cluster.error}",
		extra = "{cluster.extra}"
	)

	cellranger_chemistry_cluster_config_script = """--cluster="sbatch --cpus-per-task={core} --mem={memory} --partition={partition} --time={time} --mail-type=ALL --job-name={jobname} --output={workdir}/snakemake_log/cellranger_chemistry/{output} --error={workdir}/snakemake_log/cellranger_chemistry/{error} {extra}" """.format(
		workdir=metadata_Dict["OUTPUT"][0] + "/" + metadata_Dict["TITLE"][0],
		core="{cluster.core}",
		memory="{cluster.memory}",
		partition = "{cluster.partition}",
		time="{cluster.time}",
		jobname="{cluster.jobname}",
		output="{cluster.output}",
		error="{cluster.error}",
		extra = "{cluster.extra}"
	)

	execution_bash_script = ""
	
	execution_bash_script += """#!/bin/bash
	# +++++++++++++++++++++++++++++++++++
	# sbatch --cpus-per-task=16 --mem=16g --time=24:00:00 bash_script.sh
	module load snakemake || exit 1
	snakemake=$(which snakemake) || exit 1
	# -----------------------------------
	# +++++++++++++++++++++++++++++++++++
	echo 'GRS_SC10X Pipeline execution initiated at: '$(date)
	mkdir -p {workdir} || exit 1
	mkdir -p {workdir}/snakemake_log
	mkdir -p {workdir}/snakemake_log/cellranger_mkfastq
	mkdir -p {workdir}/snakemake_log/cellranger_chemistry
	# -----------------------------------
	# +++++++++++++++++++++++++++++++++++
	cd {workdir}/snakemake_log
	# -----------------------------------
	# +++++++++++++++++++++++++++++++++++
	""".format(
		workdir=metadata_Dict["OUTPUT"][0] + "/" + metadata_Dict["TITLE"][0],
	)

	execution_bash_script += """
	$snakemake \\
	--snakefile {GRS_SC10X_dir}/snakemake/snakemake_files/cellranger_mkfastq.smk \\
	--configfile {execution_json} \\
	--cores --unlock
	""".format(
		GRS_SC10X_dir=GRS_SC10X_directory,
		execution_json=execution_json_file_Path
	)
	
	

	if metadata_Dict["MODE"][0] == "local":
		#
		execution_bash_script += """
		
		$snakemake \
			--snakefile {GRS_SC10X_dir}/snakemake/snakemake_files/cellranger_mkfastq.smk \
			--configfile {execution_json} --keep-going --rerun-incomplete --cores --rerun-triggers mtime

		$snakemake \
			--snakefile {GRS_SC10X_dir}/snakemake/snakemake_files/cellranger_chemistry.smk \
			--configfile {execution_json} --keep-going --rerun-incomplete --cores --rerun-triggers mtime 
		""".format(
			GRS_SC10X_dir=GRS_SC10X_directory,
			execution_json=execution_json_file_Path
		)
	
	elif metadata_Dict["MODE"][0] == "slurm":
		#
		execution_bash_script += """
		
		$snakemake \
			--snakefile {GRS_SC10X_dir}/snakemake/snakemake_files/cellranger_mkfastq.smk \
			--configfile {execution_json} --cores \
			--cluster-config {GRS_SC10X_dir}/execution/cluster_production.yaml \
			--jobs=10 --max-jobs-per-second=1 --max-status-checks-per-second=0.01 --latency-wait=120 --keep-going --rerun-incomplete --rerun-triggers mtime """.format(
			GRS_SC10X_dir=GRS_SC10X_directory,
			execution_json=execution_json_file_Path
		) +  cellranger_mkfastq_cluster_config_script + """
			
		
		$snakemake \
			--snakefile {GRS_SC10X_dir}/snakemake/snakemake_files/cellranger_chemistry.smk \
			--configfile {execution_json} --cores \
			--cluster-config {GRS_SC10X_dir}/execution/cluster_production.yaml \
			--jobs=10 --max-jobs-per-second=1 --max-status-checks-per-second=0.01 --latency-wait=120 --keep-going --rerun-incomplete --rerun-triggers mtime """.format(
			GRS_SC10X_dir=GRS_SC10X_directory,
			execution_json=execution_json_file_Path
		) +  cellranger_chemistry_cluster_config_script
	else:
		#
		pass
	execution_bash_script += """
	# ##
	echo 'GRS_SC10X pipeline execution completed at: '$(date)
	# ################################### FINITO ##################################### #
	"""
	execution_bash_script = execution_bash_script.replace("\t", "")

	with open(execution_bash_file_Path, "w") as execution_bash:
		execution_bash.write(execution_bash_script)
	
	return True
	

	
# ################################### MAIN ####################################### #
def main():
	# Sanity check for usage
	if len(sys.argv) == 1:
		# Nothing was provided
		print("metadata is missing")
		print("ABORTING!!!")
		sys.exit(2)

	metadata_file_Path = sys.argv[1]
	execution_json = os.path.basename(metadata_file_Path).replace("_GRS_SC10X_metadata.csv", "_GRS_SC10X_execution.json")
	execution_bash = os.path.basename(metadata_file_Path).replace("_GRS_SC10X_metadata.csv", "_GRS_SC10X_execution.sh")
	execution_json_file_Path = os.path.dirname(os.path.realpath(metadata_file_Path)) + "/" +  execution_json
	execution_bash_file_Path = os.path.dirname(os.path.realpath(metadata_file_Path)) + "/" + execution_bash

	# +++++++++++++++++++++++++++++++
	# -------------------------------
	processed_metadata_Dict = process_metadata(metadata_file_Path)
	processed_reference_Dict = process_reference(os.path.dirname(__file__))
	build_execution_metadata(processed_metadata_Dict, processed_reference_Dict, execution_json_file_Path)

	build_execution_bash(processed_metadata_Dict, execution_json_file_Path, execution_bash_file_Path)


if __name__ == '__main__':
	main()
# ################################### FINITO ##################################### #