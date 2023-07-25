<div align="center">
   
  <h1>GRS_SC10X</h1>
  
  **_A pipeline for 10X cellranger_**

  
  <i>
    Aim: streamline and simplify 10X cellranger process
  </i>
</div>


## Overview
GRS_SC10X try to simplify and streamline cellranger process based on different chemistry.

## Dependencies
**Requires:** `snakemake>=6.0`


## Installation

### NIH_HPC(Biowulf)
Please clone this repository using the following commands:
```bash
# Clone Repository from Github
git clone https://github.com/OpenOmics/GRS_SC10X.git
cd GRS_SC10X/

# Get usage information
python ./grs_sc10x.py -h
```


### Execution-fastq

```bash
python grs_sc10x.py run \
--title sc_gex_fastq \
--input /data/RTB_GRS/ActiveProjects/user_project/cellranger_mkfastq_0204_AHLYKTBGXM/HLYKTBGXM/ \
--input-type fastq \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
##
cd /data/$USER/Test_Space/GRS_SC10X/sc_gex_fastq
sbatch --cpus-per-task=16 --mem=16g --time=24:00:00 sc_gex_fastq_GRS_SC10X_execution.sh
```

### Execution-bcl

```bash
python grs_sc10x.py run \
--title sc_gex_bcl \
--input /data/RTB_GRS/SequencerRuns/GRS_0088_Wishart/230324_NS500353_0204_AHLYKTBGXM/ \
--input-type bcl \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/user_project/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--sample-sheet /data/RTB_GRS/ActiveProjects/user_project/cellranger_mkfastq_0204_AHLYKTBGXM/CellRanger_SampleSheet_GRS_0088.csv \
--mode slurm
##
cd /data/$USER/Test_Space/GRS_SC10X/sc_gex_bcl
sbatch --cpus-per-task=16 --mem=16g --time=24:00:00 sc_gex_bcl_GRS_SC10X_execution.sh
```

## References
<sup>**2.**  Koster, J. and S. Rahmann (2018). "Snakemake-a scalable bioinformatics workflow engine." Bioinformatics 34(20): 3600.</sup>  
