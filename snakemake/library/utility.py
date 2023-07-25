# ################################### INFO ######################################## #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: Snakemake pipeline for cellranger
# ################################### IMPORT ###################################### #


import os
import sys
import re
import glob
import pandas
# ################################### INCLUDE ##################################### #
# ################################### FUNCTIONS ################################### #

def parse_run_Info(input_samplesheet_file_Path):
	"""
	"""
	#print(input_samplesheet_file_Path)
	run_Info_Dict = {}
	f = open(input_samplesheet_file_Path + "/RunInfo.xml")
	flowcell_Id = None
	Run_Id = None
	for i in f:
		if '<Run Id="' in i:
			Run_Id = i.split('<Run Id="')[1].split('"')[0].strip()
		if "<Flowcell>" in i:
			flowcell_Id = i.split("<Flowcell>")[1].split("</Flowcell>")[0].strip()
		else:
			continue
	else:
		pass
	return (Run_Id, flowcell_Id)


def build_sample_sheet_dict(config_Dict):
	"""
	"""
	sample_sheet_Dict = {}
	if "SAMPLESHEET" in config_Dict:
		#
		input_sample_sheet = config_Dict["SAMPLESHEET"][0]
	else:
		input_sample_sheet= config_Dict["DESIGN"][0]
	input_dir_List = config_Dict["INPUT"]

	for each_input_path in input_dir_List:
		##
		input_sample_sheet_Dict = parse_input_sample_sheet(input_sample_sheet)
		# print(sample_sheet_Dict)
		# print(sample_design_Dict)
		if config_Dict["INPUT_TYPE"][0] == "bcl":
			Run_Id, Flowcell_Id = parse_run_Info(each_input_path)
		else:
			Run_Id = "FASTQ_Run_Id_" + str(input_dir_List.index(each_input_path))
			Flowcell_Id = "FASTQ_Flowcell_Id_" + str(input_dir_List.index(each_input_path))
			Lane = "*"
		if Run_Id is None:
			print("unusual bcl run please check factory.parse_run_Info")
			sys.exit(2)
		elif Flowcell_Id is None:
			print("unusual bcl run please check factory.parse_run_Info")
			sys.exit(2)
		for each_sample in input_sample_sheet_Dict["Sample"]:
			##
			each_sample_index = input_sample_sheet_Dict["Sample"].index(each_sample)
			
			if config_Dict["INPUT_TYPE"][0] == "bcl":
				#
				Lane = input_sample_sheet_Dict["Lane"][each_sample_index]
			else:
				Lane = "*"
			if each_sample not in sample_sheet_Dict:
				#
				sample_sheet_Dict[each_sample] = {}
				sample_sheet_Dict[each_sample]["input_path"] = [each_input_path]
				sample_sheet_Dict[each_sample]["Flowcell_Id"] = [Flowcell_Id]
				sample_sheet_Dict[each_sample]["Run_Id"] = [Run_Id]
				sample_sheet_Dict[each_sample]["Lane"] = [Lane]
				#
			else:
				#
				sample_sheet_Dict[each_sample]["input_path"].append(each_input_path)
				sample_sheet_Dict[each_sample]["Flowcell_Id"].append(Flowcell_Id)
				sample_sheet_Dict[each_sample]["Run_Id"].append(Run_Id)
				sample_sheet_Dict[each_sample]["Lane"].append(Lane)
		else:
			##for each_sample in input_sample_sheet_Dict["Sample"]:
			pass
				
	else:
		##for each_input_path in input_dir_List:
		pass
	for each_sample in sample_sheet_Dict:
		sample_sheet_Dict[each_sample]["input_path"] = sample_sheet_Dict[each_sample]["input_path"]
		sample_sheet_Dict[each_sample]["Flowcell_Id"] = sample_sheet_Dict[each_sample]["Flowcell_Id"]
		sample_sheet_Dict[each_sample]["Run_Id"] = sample_sheet_Dict[each_sample]["Run_Id"]
		sample_sheet_Dict[each_sample]["Lane"] = sample_sheet_Dict[each_sample]["Lane"]
	else:
		pass
	return sample_sheet_Dict


def parse_input_sample_sheet(input_samplesheet_file_path):
	"""
	"""
	sample_sheet_Dict = {}
	samplesheet_DF = pandas.read_csv(
		input_samplesheet_file_path,
		encoding=None,
		skip_blank_lines=True,
		delimiter=",",
		index_col=None
	)
	sample_sheet_Dict = samplesheet_DF.fillna('empty').to_dict('list')
	return sample_sheet_Dict


def build_sample_metadata_dict(config_Dict):
	"""
	item is one row of design table
	step1: build original dict
	step2 parse dict int mor organized one
	step3 add additional chemistry for aggregate
	"""
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	#step0
	sample_sheet_Dict = build_sample_sheet_dict(config_Dict)
	# ------------------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	sample_metadata_Dict = {}
	temp_design_Dict = {}
	#step1
	design_DF = pandas.read_csv(
		config_Dict["DESIGN"][0],
		encoding=None,
		skip_blank_lines=True,
		delimiter=",",
		index_col=None
	)
	design_DF["Chemistry"] = design_DF["Chemistry"].str.lower()
	design_List = design_DF.fillna('empty').to_dict('records')
	#step2
	for each_item in design_List:
		##
		design = each_item["Design"]
		chemistry = each_item["Chemistry"]
		sample = each_item["Sample"]
		if design not in temp_design_Dict:
			#
			temp_design_Dict[design] = {}
			temp_design_Dict[design][chemistry] = {}
			temp_design_Dict[design][chemistry][sample] = {**each_item, **sample_sheet_Dict[sample]}
			
		elif chemistry not in temp_design_Dict[design]:
			#
			temp_design_Dict[design][chemistry] = {}
			temp_design_Dict[design][chemistry][sample] = {**each_item, **sample_sheet_Dict[sample]}
			
		elif sample not in temp_design_Dict[design][chemistry]:
			#
			temp_design_Dict[design][chemistry][sample] = {**each_item, **sample_sheet_Dict[sample]}
			
		else:
			#
			pass
	else:
		pass
	# ------------------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	#step3
	for each_design in temp_design_Dict:
		##
		for each_chemistry in list(temp_design_Dict[each_design]):
			##
			sample_List = temp_design_Dict[each_design][each_chemistry].keys()
			if len(sample_List) > 1:
				#
				aggregate_chemistry = each_chemistry  + "_aggr"
				temp_design_Dict[each_design][aggregate_chemistry] = temp_design_Dict[each_design][each_chemistry]
			else:
				pass
		else:
			pass
	else:
		pass
	# ------------------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	sample_metadata_Dict = temp_design_Dict
	# ------------------------------------------------------------
	return sample_metadata_Dict


def build_snakemake_IO_dict(config_Dict, sample_metadata_Dict):
	
	"""
	Step1: find the input of the rule
	Step2: build the output of the rule
	"""
	
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	IO_Dict = {}
	IO_Dict["snakefile"] = {}
	IO_Dict["snakefile_target_List"] = []
	# ------------------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	last_snakefile = "cellranger"
	last_snakefile_output = "{work_dir}/{title}/{snakefile}/".format(
		work_dir=config_Dict["OUTPUT"][0], 
		title=config_Dict["TITLE"][0], 
		snakefile=last_snakefile,
	)

	snakefile = "cellranger"
	snakefile_output = "{work_dir}/{title}/{snakefile}/".format(
		work_dir=config_Dict["OUTPUT"][0], 
		title=config_Dict["TITLE"][0], 
		snakefile=snakefile
	)
	# ------------------------------------------------------------
	for design in sample_metadata_Dict:
		##
		IO_Dict["snakefile"][design] = {}
		for chemistry in sample_metadata_Dict[design]:
			##
			if chemistry in ["gex", "vdj", "atac"]:
				#
				last_snakerule = "cellranger_mkfastq"
				snakerule = "cellranger_" + chemistry
				IO_Dict["snakefile"][design][snakerule] = {}
				
				for sample in sample_metadata_Dict[design][chemistry]:
					##
					# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#step1
					
					last_snakerule_target_List = []
					for each_Run_Id in sample_metadata_Dict[design][chemistry][sample]["Run_Id"]:
						##
						for each_Flowcell_Id in sample_metadata_Dict[design][chemistry][sample]["Flowcell_Id"]:
							##
							
							last_snakerule_target_List.extend(glob.glob(
								last_snakefile_output + "{snakerule}/{Run_Id}/{Flowcell_Id}/target/{Flowcell_Id}.{snakerule}.target".format(
								Run_Id=each_Run_Id,
								Flowcell_Id=each_Flowcell_Id, 
								snakerule=last_snakerule
								)))
						else:
							##
							pass
					
					# ------------------------------------------------------------
					# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					#step2
					# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					snakerule_output = "{prefix}{snakerule}/{design}/{sample}/".format(
						prefix=snakefile_output,
						design=design,
						sample=sample,
						snakerule=snakerule
					)
					# ------------------------------------------------------------
					# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					snakerule_target_path = snakerule_output + "target/"
					snakerule_target = "{prefix}{sample}{suffix}".format(
						prefix=snakerule_target_path, 
						sample=sample, 
						suffix="." + snakerule + ".target"
					)
					# -------------------------------------------------------------
					# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
					IO_Dict["snakefile"][design][snakerule][sample] = {}
					IO_Dict["snakefile"][design][snakerule][sample]["snakemake_input"] = list(set(last_snakerule_target_List))
					IO_Dict["snakefile"][design][snakerule][sample]["snakemake_rule_input"] = list(set(last_snakerule_target_List))
					IO_Dict["snakefile"][design][snakerule][sample]["snakemake_output"] = snakerule_target
					IO_Dict["snakefile_target_List"].append(snakerule_target)
					# ------------------------------------------------------------
				else:
					##for sample in sample_chemistry_design_Dict[design][chemistry]:
					pass
			elif chemistry in ["fbc"]:
				#if chemistry in ["gex", "vdj", "atac"]:
				last_snakerule = "cellranger_mkfastq"
				snakerule = "cellranger_" + chemistry
				IO_Dict["snakefile"][design][snakerule] = {}
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				#Step1
				fbc_input_Dict = {}
				fbc_input_Dict["gex"] = {}
				fbc_input_Dict["fbc"] = {}
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				for sample in sample_metadata_Dict[design]["fbc"]:
					##
					last_snakerule_target_List = []
					for each_Run_Id in sample_metadata_Dict[design]["fbc"][sample]["Run_Id"]:
						##
						for each_Flowcell_Id in sample_metadata_Dict[design]["fbc"][sample]["Flowcell_Id"]:
							##
							
							last_snakerule_target_List.extend(glob.glob(
								last_snakefile_output + "{snakerule}/{Run_Id}/{Flowcell_Id}/target/{Flowcell_Id}.{snakerule}.target".format(
								Run_Id=each_Run_Id,
								Flowcell_Id=each_Flowcell_Id, 
								snakerule=last_snakerule
								)))
							
						else:
							##
							pass
					else:
						fbc_input_Dict["fbc"][sample] = list(set(last_snakerule_target_List))
				else:
					##for sample in sample_chemistry_design_Dict[design][chemistry]:
					pass
				# -------------------------------------------------------------
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				for sample in sample_metadata_Dict[design]["gex"]:
					##
					last_snakerule_target_List = []
					for each_Run_Id in sample_metadata_Dict[design]["gex"][sample]["Run_Id"]:
						##
						for each_Flowcell_Id in sample_metadata_Dict[design]["gex"][sample]["Flowcell_Id"]:
							##
							
							last_snakerule_target_List.extend(glob.glob(
								last_snakefile_output + "{snakerule}/{Run_Id}/{Flowcell_Id}/target/{Flowcell_Id}.{snakerule}.target".format(
								Run_Id=each_Run_Id,
								Flowcell_Id=each_Flowcell_Id, 
								snakerule=last_snakerule
								)))
							
						else:
							##
							pass
					else:
						fbc_input_Dict["gex"][sample] = list(set(last_snakerule_target_List))
				else:
					##for sample in sample_chemistry_design_Dict[design][chemistry]:
					pass
				# -------------------------------------------------------------
				# -------------------------------------------------------------
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				#Step2
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				gex_sample_List = sorted(list(set(fbc_input_Dict["gex"].keys())))
				fbc_sample_List = sorted(list(set(fbc_input_Dict["fbc"].keys())))
				fbc_sample_title = "FBC_" + "_".join(fbc_sample_List) + "_and_GEX_" + "_".join(gex_sample_List)
				# ------------------------------------------------------------
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				snakerule_output = "{prefix}{snakerule}/{design}/{sample}/".format(
					prefix=snakefile_output,
					design=design,
					sample=fbc_sample_title,
					snakerule=snakerule
				)
				# ------------------------------------------------------------
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				snakerule_target_path = snakerule_output + "target/"
				snakerule_target = "{prefix}{sample}{suffix}".format(
					prefix=snakerule_target_path, 
					sample=fbc_sample_title, 
					suffix="." + snakerule + ".target"
				)
				# -------------------------------------------------------------
				# -------------------------------------------------------------
				
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				fbc_first_element = list(fbc_input_Dict["fbc"].keys())[0]
				
				IO_Dict["snakefile"][design][snakerule][fbc_sample_title] = {}
				IO_Dict["snakefile"][design][snakerule][fbc_sample_title]["snakemake_input"] = fbc_input_Dict
				IO_Dict["snakefile"][design][snakerule][fbc_sample_title]["snakemake_rule_input"] = fbc_input_Dict["fbc"][fbc_first_element]
				IO_Dict["snakefile"][design][snakerule][fbc_sample_title]["snakemake_output"] = snakerule_target
				IO_Dict["snakefile_target_List"].append(snakerule_target)
				# ------------------------------------------------------------
				

			elif chemistry in ["gex_aggr", "vdj_aggr", "atac_aggr"]:
				#if chemistry in ["gex", "vdj", "atac"]:
				last_snakerule = "cellranger_" + chemistry.split("_aggr")[0] 
				snakerule = "cellranger_" + chemistry
				IO_Dict["snakefile"][design][snakerule] = {}
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				#Step1
				last_snakerule_target_List = []
				for sample in sample_metadata_Dict[design][chemistry]:
					last_snakerule_target_List.append(IO_Dict["snakefile"][design][last_snakerule][sample]["snakemake_output"])
				else:
					pass
				# -------------------------------------------------------------
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				#Step2
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				aggr_sample_List = sorted(list(set(sample_metadata_Dict[design][chemistry].keys())))
				
				aggr_sample_title = chemistry  + "_" + design + "_" + "_".join(aggr_sample_List)
				# ------------------------------------------------------------
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				snakerule_output = "{prefix}{snakerule}/{design}/{sample}/".format(
					prefix=snakefile_output,
					design=design,
					sample=aggr_sample_title,
					snakerule=snakerule
				)
				# ------------------------------------------------------------
				# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
				snakerule_target_path = snakerule_output + "target/"
				snakerule_target = "{prefix}{sample}{suffix}".format(
					prefix=snakerule_target_path, 
					sample=aggr_sample_title, 
					suffix="." + snakerule + ".target"
				)
				# -------------------------------------------------------------
				# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

				IO_Dict["snakefile"][design][snakerule][aggr_sample_title] = {}
				IO_Dict["snakefile"][design][snakerule][aggr_sample_title]["snakemake_input"] = last_snakerule_target_List
				IO_Dict["snakefile"][design][snakerule][aggr_sample_title]["snakemake_rule_input"] = last_snakerule_target_List
				IO_Dict["snakefile"][design][snakerule][aggr_sample_title]["snakemake_output"] = snakerule_target
				IO_Dict["snakefile_target_List"].append(snakerule_target)
				# -------------------------------------------------------------
				# -------------------------------------------------------------
			else:
				#if chemistry in ["gex", "vdj", "atac"]:
				pass

		else:
			##for chemistry in sample_chemistry_design_Dict[design]:
			pass
	else:
		##for design in sample_chemistry_design_Dict:
		pass
	
	return IO_Dict


def build_cellranger_mkfastq_IO_dict(config_Dict, sample_metadata_Dict):
	"""
	"""
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	input_path_List = []
	Flowcell_Id_List = []
	Run_Id_List = []
	for design in sample_metadata_Dict:
		##
		for chemistry in sample_metadata_Dict[design]:
			##
			for sample in sample_metadata_Dict[design][chemistry]:
				##
				for each_input_path in sample_metadata_Dict[design][chemistry][sample]['input_path']:
					#
					if each_input_path not in input_path_List:
						input_path_List.append(each_input_path)
					else:
						#
						pass
				else:
					#
					pass
				for each_item in sample_metadata_Dict[design][chemistry][sample]['Flowcell_Id']:
					#
					if each_item not in Flowcell_Id_List:
						Flowcell_Id_List.append(each_item)
					else:
						#
						pass
				else:
					#
					pass
				for each_item in sample_metadata_Dict[design][chemistry][sample]['Run_Id']:
					#
					if each_item not in Run_Id_List:
						Run_Id_List.append(each_item)
					else:
						#
						pass
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
		pass
	
	# ------------------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	snakefile = "cellranger"
	snakefile_output = "{work_dir}/{title}/{snakefile}/".format(
		work_dir=config_Dict["OUTPUT"][0], 
		title=config_Dict["TITLE"][0], 
		snakefile=snakefile
	)
	# ------------------------------------------------------------
	IO_Dict = {}
	IO_Dict["snakefile"] = {}
	IO_Dict["snakefile"]["snakefile_target_List"] = []
	snakerule = "cellranger_mkfastq"
	for each_input_path, each_Flowcell_Id, each_Run_ID in zip(input_path_List, Flowcell_Id_List, Run_Id_List):
		##
		sample = each_Flowcell_Id
		design = each_Run_ID
		if design not in IO_Dict["snakefile"]:
			#
			IO_Dict["snakefile"][design] = {}
		if snakerule not in IO_Dict["snakefile"][design]:
			#
			IO_Dict["snakefile"][design][snakerule] = {}
		if sample not in IO_Dict["snakefile"][design][snakerule]:
			#
			IO_Dict["snakefile"][design][snakerule][sample] = {}
		else:
			#
			pass
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		snakerule_output = "{prefix}{snakerule}/{design}/{sample}/".format(
			prefix=snakefile_output,
			design=design,
			sample=sample,
			snakerule=snakerule
		)
		# ------------------------------------------------------------
		# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		snakerule_target_path = snakerule_output + "target/"
		snakerule_target = "{prefix}{sample}{suffix}".format(
			prefix=snakerule_target_path, 
			sample=sample, 
			suffix="." + snakerule + ".target"
		)
		# -------------------------------------------------------------
		# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
		IO_Dict["snakefile"][design][snakerule][sample]["snakemake_input"] = [each_input_path]
		IO_Dict["snakefile"][design][snakerule][sample]["snakemake_rule_input"] = [each_input_path]
		IO_Dict["snakefile"][design][snakerule][sample]["snakemake_output"] = [snakerule_target]
		IO_Dict["snakefile"]["snakefile_target_List"].append(snakerule_target)
		# ------------------------------------------------------------
	else:
		##
		pass
	return IO_Dict
# ################################### CONFIGURATION ############################### #
# ################################### WILDCARDS ################################### #
# ################################### PIPELINE FLOW ############################### #
# ################################### PIPELINE RULES ############################## #
# ################################### FINITO ###################################### #