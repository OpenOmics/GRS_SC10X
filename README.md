<div align="center">
   
  <h1>GRS_SC10X</h1>
  
  **_A pipeline for 10X cellranger_**

  
  <i>
    This is the home of the pipeline, GRS_SC10X. <br>
    Aim: streamline and simplify 10X cellranger process
  </i>
</div>


## Overview
GRS_SC10X try to simplify and streamline cellranger process based on different chemistry.

## Dependencies
**Requires:** `snakemake>=6.0`


## Installation

### Biowulf
Please clone this repository using the following commands:
```bash
# Clone Repository from Github
git clone https://github.com/OpenOmics/GRS_SC10X.git
cd GRS_SC10X/

# Get usage information
./grs_sc10x.py -h
```


### Execution-fastq

```bash
grs_sc10x.py run \
--title sc_gex_fastq \
--input /data/RTB_GRS/ActiveProjects/user_project/cellranger_mkfastq_0204_AHLYKTBGXM/HLYKTBGXM/ \
--input-type fastq \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
```

### Execution-bcl

```bash
/grs_sc10x.py run \
--title sc_gex_bcl \
--input /data/RTB_GRS/SequencerRuns/GRS_0088_Wishart/230324_NS500353_0204_AHLYKTBGXM/ \
--input-type bcl \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/user_project/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--sample-sheet /data/RTB_GRS/ActiveProjects/user_project/cellranger_mkfastq_0204_AHLYKTBGXM/CellRanger_SampleSheet_GRS_0088.csv \
--mode slurm
```

## References
<sup>**2.**  Koster, J. and S. Rahmann (2018). "Snakemake-a scalable bioinformatics workflow engine." Bioinformatics 34(20): 3600.</sup>  
