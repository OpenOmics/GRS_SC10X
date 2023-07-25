#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ################################### INFO ####################################### #
# Author: Amir Shams
# Project: GRS_SC10X
# Aim: pipeline for cellranger
# ################################### IMPORT ##################################### #

import os, sys
import argparse
import textwrap
import subprocess
import pandas
# ################################### CONSTANT ################################## #
__author__   = 'Amir Shams'
__version__  = 'v0.0.1'
__email__    = 'shamsaddinisha@nih.gov'
__home__     =  os.path.dirname(os.path.abspath(__file__))
_name       = os.path.basename(sys.argv[0])
_description = 'pipeline to process singlecell data'
# ################################### FUNCTIONS ################################ #


class Colors():
	"""Class encoding for ANSI escape sequeces for styling terminal text.
	Any string that is formatting with these styles must be terminated with
	the escape sequence, i.e. `Colors.end`.
	"""
	# Escape sequence
	end = '\33[0m'
	# Formatting options
	bold   = '\33[1m'
	italic = '\33[3m'
	url    = '\33[4m'
	blink  = '\33[5m'
	higlighted = '\33[7m'
	# Text Colors
	black  = '\33[30m'
	red    = '\33[31m'
	green  = '\33[32m'
	yellow = '\33[33m'
	blue   = '\33[34m'
	pink  = '\33[35m'
	cyan  = '\33[96m'
	white = '\33[37m'
	# Background fill colors
	bg_black  = '\33[40m'
	bg_red    = '\33[41m'
	bg_green  = '\33[42m'
	bg_yellow = '\33[43m'
	bg_blue   = '\33[44m'
	bg_pink  = '\33[45m'
	bg_cyan  = '\33[46m'
	bg_white = '\33[47m'


def build_help(name, description):
	"""
	"""

	# Add styled name and description
	c = Colors
	styled_name = "{0}{1}{2}cell{3}_seek{4}".format(c.bold, c.bg_black, c.white, c.cyan, c.end)
	description = "{0}{1}{2}".format(c.bold, description, c.end)

	generated_help = textwrap.dedent(
		"""
		{1}{0} {3}run{4}: {1} Runs the GRS_SC10X pipeline.{4}

		{1}{2}Synopsis:{4}
		  $ {0} run [--help] \\
							  [--sample-sheet SAMPLE SHEET FILE] \\
							  --input INPUT [INPUT ...] \\
							  --output OUTPUT \\
							  --title TITLE \\
							  --host {{mouse, human}} \\
							  --input-type {{bcl, fastq}} \\
							  --design DESIGN FILE \\
							  --mode {{slurm, local}}

		{1}{2}Description:{4}
		
		To run the pipeline with with your data, please provide a space seperated 
		list of directories contaning fastq or bcl files, an output directory to store results, 
		provide a title for your project and select host from provided options.
		provide the path to your design file(metadat including Library ID, Chemistry, Design, Index and custom reference).
		if you have bcl file you need to provide 10X sample-sheet file path
		and a select mode of execution from provided options. 

		Optional arguments are shown in square brackets above. Please visit our docs
		at "https://soon will be provided" for more information, examples, and 
		guides. 

		{1}{2}Required arguments:{4}
		--input INPUT_PATH [INPUT ...]
								Directories(space separated) containing fastq files or BCL directories(space separate) related to your 10X experiment .
								
									Example: --input /path/to/your/fastq_dir
									Example: --input /path/to/your/bcl_dir1 /path/to/your/bcl_dir2
		--input-type {{bcl, fastq}}
								you can select the input type from fastq or bcl file
									Example: --input-type fastq

		--output OUTPUT_PATH
								Path to an output directory. This path is the location where the specified folder(--title) will be created
									Example: --output /data/$USER/working_directory

		--title TITLE
								title will be a directory in specifed output(--output) where store all generated files.
									Example: --title my_experiment_1
	
		--host {{human, mouse}}
								Reference genome. GRS_SC10X will use pre-built pipline
									Example: --host human
		--design DESIGN_FILE_PATH
								A CSV metadata file containing information about each sample. 
								It contains each sample's name, design, Index, Chemistry, Index_Type, custom_reference
								Here is an example design.csv file:
									Sample,Design,Index,Chemistry,Index_Type,custom_reference
									LIB_02356_01,Group1,SI-TT-E3,GEX,Dual_Index,
									LIB_02357_01,Group1,SI-TT-F3,FBC,Dual_Index,/path/to/my/HTO/library
									LIB_02358_01,Group2,SI-TT-F4,VDJ,Dual_Index,
								where:
								1-Sample: name of the sample passed to CellRanger.
								2-Design: category which you want this sample to be included
								3-Index: specified chemistry index
								4-Chemistry: librart or chemistry type of this sample
								5-Index_Type: type of Index based on 10X guidance
								6-custom_reference: this is the custom reference which you want your FBC(antibody reference) 
								or HTO(hash tagging reference) custom reference to align against.
								Example --design my_design.csv
		--sample-sheet {{only required for bcl input}} SAMPLE_SHEET_FILE_PATH
								if you select bcl as your input type(--input-type) then you have to provide 10X standard sample-sheet file path
		
		{1}{2}Misc Options:{4}
		  -h, --help            Show usage information, help message, and exit.
								  Example: --help
		""".format(name, c.bold, c.url, c.italic, c.end)
	)

	return generated_help
	


def fatal(*message, **kwargs):
	"""Prints any provided args to standard error
	and exits with an exit code of 1.
	@param message <any>:
		Values printed to standard error
	@params kwargs <print()>
		Key words to modify print function behavior
	"""
	
	err(*message, **kwargs)
	sys.exit(1)


def err(*message, **kwargs):
	"""Prints any provided args to standard error.
	kwargs can be provided to modify print functions 
	behavior.
	@param message <any>:
		Values printed to standard error
	@params kwargs <print()>
		Key words to modify print function behavior
	"""
	print(*message, file=sys.stderr, **kwargs)


def exists(testpath):
	"""Checks if file exists on the local filesystem.
	@param parser <argparse.ArgumentParser() object>:
		argparse parser object
	@param testpath <str>:
		Name of file/directory to check
	@return does_exist <boolean>:
		True when file/directory exists, False when file/directory does not exist
	"""
	does_exist = True
	if not os.path.exists(testpath):
		does_exist = False # File or directory does not exist on the filesystem

	return does_exist

def is_path_writeable(parser, the_Path):
	"""
	"""
	if os.path.exists(the_Path) and os.access(the_Path, os.W_OK) and os.access(the_Path, os.R_OK):
		#
		return the_Path
	else:
		parser.error("--output '{}' is not accessible,either it is not available or wrong permissions!".format(the_Path))


def is_path_readable(parser, the_Path):
	"""
	"""
	if os.path.exists(the_Path) and os.access(the_Path, os.R_OK):
		#
		return the_Path
	else:
		parser.error("--input '{}' is not accessible,either it is not available or wrong permissions!".format(the_Path))


def is_sample_sheet_required(parser, sample_sheet_file_Path):
	"""
	"""
	print("hello")
	if sample_sheet_file_Path is None and sub_args.input_type == "bcl":
		#
		parser.error("sample_sheet file is required when yu select bcl file")
	else:
		return sample_sheet_file_Path


def initialize(sub_args):
	"""
	"""
	if not exists(sub_args.output):
		# Pipeline output directory does not exist on filesystem
		os.makedirs(sub_args.output)
	elif exists(sub_args.output) and not exists(os.path.join(sub_args.output, sub_args.title)):
		#
		os.makedirs(os.path.join(sub_args.output, sub_args.title))
	elif exists(os.path.join(sub_args.output, sub_args.title)) and os.path.isfile(os.path.join(sub_args.output, sub_args.title)):
		# Provided Path for pipeline output directory exists as file
		raise OSError("""\n\tFatal: Failed to create provided pipeline output directory!
		User provided --output PATH already exists on the filesystem as a file.
		Please run {} again with a different --output PATH.
		""".format(sys.argv[0])
		)
	return True


def unlock(sub_args):
	"""
	"""
	# Initialize working directory, copy over required pipeline resources
	initialize(output_path = sub_args.output)
	#we buils GRS_SC10X csv file
	pipeline_string = ""
	pipeline_string += "title," + sub_args.title + "\n"
	pipeline_string += "host," + sub_args.host + "\n"
	pipeline_string += "output," + sub_args.output + "\n"
	pipeline_string += "libraries," + sub_args.libraries + "\n"
	metadata_file_Path = open(os.path.join(sub_args.output, '/', sub_args.title, '_GRS_SC10X.csv'), 'w')
	metadata_file_Path.write(pipeline_string)
	metadata_file_Path.close()
	
	return True


def run(sub_args):
	"""
	"""
	# print("hello")
	# print(sub_args)
	# Initialize working directory, copy over required pipeline resources
	initialize(sub_args)
	metadata_Dict = {}
	metadata_Dict["title"] = sub_args.title
	metadata_Dict["host"] = sub_args.host 
	metadata_Dict["input-type"] = sub_args.input_type

	if sub_args.sample_sheet is None:
		#
		metadata_Dict["sample-sheet"] = None
	else:
		#
		metadata_Dict["sample-sheet"] = sub_args.sample_sheet.name
	
	metadata_Dict["input"] = ";".join(sub_args.input)
	
	metadata_Dict["output"] = sub_args.output
	metadata_Dict["design"] = sub_args.design.name
	metadata_Dict["mode"] = sub_args.mode 
	
	metadata_DF = pandas.DataFrame(metadata_Dict.items())
	metadata_DF.to_csv(os.path.join(sub_args.output, sub_args.title, sub_args.title +  '_GRS_SC10X_metadata.csv'), index=False, header=False)

	# ----------------------------------------------------
	# ++++++++++++++++++++++++++++++++++++++++++++++++++++

	#we call specified bash script
	GRS_SC10X_file_Path = os.path.dirname(os.path.realpath(__file__))
	build_execution_json_python = GRS_SC10X_file_Path + '/execution/GRS_SC10X_build_execution_json.py'
	build_execution_scrip_bash = GRS_SC10X_file_Path + '/execution/GRS_SC10X_build_execution_bash.py'
	GRS_SC10X_metadata_path = os.path.join(sub_args.output, sub_args.title, sub_args.title +  '_GRS_SC10X_metadata.csv')
	working_directory = os.path.join(sub_args.output, sub_args.title)
	# process = subprocess.Popen(
	# 	['/usr/bin/bash', run_GRS_SC10X_bash, GRS_SC10X_metadata_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
	# 	)
	process = subprocess.Popen(
		['python', build_execution_json_python, GRS_SC10X_metadata_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
		)
	stdout, stderr = process.communicate()
	print(stdout)
	print(stderr)
	if int(process.returncode) == 0:
		print('{} pipeline has successfully completed'.format(_name))
	else:
		fatal('{} pipeline failed. Please see standard output for more information.')
	return True


def parsed_arguments(name, description):
	"""
	"""
	# +++++++++++++++++++++++++++++++++++++++++++++++++++
	 # Add styled name and description
	c = Colors
	styled_name = "{0}cell-seek{1}".format(c.bold, c.end)
	description = "{0}{1}{2}".format(c.bold, description, c.end)
	# ---------------------------------------------------
	# +++++++++++++++++++++++++++++++++++++++++++++++++++
	# Create a top-level parser
	parser = argparse.ArgumentParser(description = '{}: {}'.format(styled_name, description))
	# ---------------------------------------------------
	# +++++++++++++++++++++++++++++++++++++++++++++++++++
	# Adding Verison information
	parser.add_argument('--version', action = 'version', version='%(prog)s {}'.format(__version__))
	# Create sub-command parser
	subparsers = parser.add_subparsers(help='List of available sub-commands')
	# ---------------------------------------------------

	generated_help_string = build_help(name, description)
	# +++++++++++++++++++++++++++++++++++++++++++++++++++
	# Options for the "run" sub-command
	subparser_run = subparsers.add_parser(
		'run',
		help = 'Run the cell-seek pipeline with your input files.',
		usage = argparse.SUPPRESS,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description = generated_help_string,
		#epilog  = run_epilog,
		add_help=False
	)

	subparser_run.add_argument(
		'-h', '--help', 
		action='help', 
		help=argparse.SUPPRESS
	)
	# Required Arguements
	subparser_run.add_argument(
		'--input',
		# Check if the file exists and if it is readable
		#type = lambda file: is_path_readable(parser, file),
		#type=list,
		required = True,
		nargs = '+',
		#action = 'append',
		help = argparse.SUPPRESS
	)

	subparser_run.add_argument(
		'--input-type',
		required = True,
		choices = ['bcl', 'fastq'],
		help = argparse.SUPPRESS
	)

	# Output Directory, 
	# analysis working directory
	subparser_run.add_argument(
		'--output',
		type = lambda file: is_path_writeable(parser, file),
		required = True,
		help = argparse.SUPPRESS
	)

	# execution title
	subparser_run.add_argument(
		'--title',
		action = 'store',
		required = True,
		help = argparse.SUPPRESS
	)

	subparser_run.add_argument(
		'--host',
		required = True,
		choices = ['human', 'mouse', 'xenomorph'],
		help = argparse.SUPPRESS
	)

	subparser_run.add_argument(
		'--design',
		#type = lambda option: os.path.abspath(os.path.expanduser(option)),
		type = argparse.FileType('r', encoding='UTF-8'),
		required = True,
		help = argparse.SUPPRESS
	)

	subparser_run.add_argument(
		'--mode',
		type = str,
		required = False,
		default = "slurm",
		choices = ['slurm', 'local'],
		help = argparse.SUPPRESS
	)
	#to make sure the sample sheet are required if bcl file detected
	opts, rem_args = subparser_run.parse_known_args()
	if opts.input_type == "bcl":
		print("bcl selected")
		subparser_run.add_argument(
			'--sample-sheet',
			type = argparse.FileType('r', encoding='UTF-8'),
			required = True,
			help = argparse.SUPPRESS
		)
	else:
		print("fastq detected")
		subparser_run.add_argument(
			'--sample-sheet',
			type = argparse.FileType('r', encoding='UTF-8'),
			required = False,
			help = argparse.SUPPRESS
		)
	# ---------------------------------------------------
	# +++++++++++++++++++++++++++++++++++++++++++++++++++
	# Supressing help message of required args to overcome no sub-parser named groups
	subparser_unlock = subparsers.add_parser(
		'unlock',
		help = 'Unlocks a previous runs output directory.',
		usage = argparse.SUPPRESS,
		formatter_class=argparse.RawDescriptionHelpFormatter,
		#description = required_unlock_options,
		#epilog = unlock_epilog,
		add_help = False
	)
	# ---------------------------------------------------


	# Define handlers for each sub-parser
	subparser_run.set_defaults(func = run)
	subparser_unlock.set_defaults(func = unlock)

	
	# Parse command-line args
	args = parser.parse_args()
	return args


# ################################### MAIN ####################################### #

def main():
	# Sanity check for usage
	if len(sys.argv) == 1:
		# Nothing was provided
		fatal('Invalid usage: {} [-h] [--version] ...'.format(_name))

	# Collect args for sub-command
	args = parsed_arguments(
		name = _name,
		description = _description
	)

	# Display version information
	print('cell-seek ({})'.format(__version__))

	# Mediator method to call sub-command's set handler function
	args.func(args)


if __name__ == '__main__':
	main()
# ################################### FINITO ##################################### #