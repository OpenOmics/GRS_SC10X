
sbatch --cpus-per-task=16 --mem=16g --time=24:00:00
# ++++++++++++++++++++++++++++++++++++++++++++++++++++

######################
#GEX
# ++++++++++++++++++++++++++++++++++++++++++++++++++++
#test fastq input
python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_gex_fastq \
--input /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/cellranger_mkfastq_0204_AHLYKTBGXM/HLYKTBGXM/ \
--input-type fastq \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# ----------------------------------------------------
# ++++++++++++++++++++++++++++++++++++++++++++++++++++

python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_gex_bcl \
--input /data/RTB_GRS/SequencerRuns/GRS_0088_Wishart/230324_NS500353_0204_AHLYKTBGXM/ \
--input-type bcl \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/wishart_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--sample-sheet /data/RTB_GRS/ActiveProjects/GRS_0088_Wishart/cellranger_mkfastq_0204_AHLYKTBGXM/CellRanger_SampleSheet_GRS_0088.csv \
--mode slurm
# ----------------------------------------------------

######################
#VDJ
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++

python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_vdj_bcl \
--input /data/RTB_GRS/SequencerRuns/GRS_0098_Lu/230407_NS500353_0205_AHM2KKBGXM/ \
--input-type bcl \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0098_Lu/Lu_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--sample-sheet /data/RTB_GRS/ActiveProjects/GRS_0098_Lu/cellranger_mkfastq_0205_AHM2KKBGXM/CellRanger_SampleSheet_GRS_0098_corrected.csv \
--mode slurm

python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_vdj_fastq \
--input /data/RTB_GRS/ActiveProjects/GRS_0098_Lu/cellranger_mkfastq_0205_AHM2KKBGXM/HM2KKBGXM/ \
--input-type fastq \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0098_Lu/Lu_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# -------------------------------------------------------


######################
#FBC
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
#FBC WITH MULTI RUN
python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_fbc_fastq \
--input /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/cellranger_mkfastq_0210_AHLYYGBGXM/HLYYGBGXM /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/cellranger_mkfastq_39_AAC3F27HV/AAC3F27HV /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/cellranger_mkfastq_50_AAC3HKGHV/AAC3HKGHV \
--input-type fastq \
--host human \
--design /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/GRS_0112_Panda_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# -------------------------------------------------------

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_fbc_bcl \
--input /data/RTB_GRS/SequencerRuns/GRS_0112_Panda/230606_VH00286_39_AAC3F27HV/ /data/RTB_GRS/SequencerRuns/GRS_0112_Panda/230510_NS500353_0210_AHLYYGBGXM/ /data/RTB_GRS/SequencerRuns/GRS_0112_Panda/230710_VH00286_50_AAC3HKGHV/ \
--input-type bcl \
--host human \
--sample-sheet /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/CellRanger_SampleSheet_GRS_0112.csv \
--design /data/RTB_GRS/ActiveProjects/GRS_0112_Panda/GRS_0112_Panda_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# -------------------------------------------------------

######################
#HTO
python /data/$USER/Development/10Xsnakepipe/grs_sc10x.py run \
--title sc_hto_fastq \
--input /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/cellranger_mkfastq_0212_AHFLJGBGXC/HFLJGBGXC/ /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/cellranger_mkfastq_0204_AHFKCFBGXC/HFKCFBGXC/ \
--input-type fastq \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/GRS_0168_Zheng_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm

python /data/$USER/Development/10Xsnakepipe/grs_sc10x.py run \
--title sc_hto_fastq \
--input /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/cellranger_mkfastq_0212_AHFLJGBGXC/HFLJGBGXC/ /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/cellranger_mkfastq_0204_AHFKCFBGXC/HFKCFBGXC/ \
--input-type bcl \
--host mouse \
--design /data/RTB_GRS/ActiveProjects/GRS_0168_Zheng/GRS_0168_Zheng_sample_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode local
# ----------------------------------------------------



######################
#ATAC
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_atac_fastq \
--input /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/cellranger_atac_mkfastq_0190/HF3MLBGXK/ /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/cellranger_atac_mkfastq_0188/HC2HKBGXK/ /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/cellranger_atac_mkfastq_0177/HF3KFBGXK/ \
--input-type fastq \
--host human \
--design /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/satya_atac_design.csv \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# -------------------------------------------------------
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++
python /data/$USER/Development/GRS_SC10X/grs_sc10x.py run \
--title sc_atac_bcl \
--input /data/RTB_GRS/SequencerRuns/NGS_0543_singh/220420_NS500189_0188_AHC2HKBGXK/ /data/RTB_GRS/SequencerRuns/NGS_0543_singh/220607_NS500189_0190_AHF3MLBGXK/ /data/RTB_GRS/SequencerRuns/NGS_0543_singh/220608_NS500353_0177_AHF3KFBGXK/ \
--input-type bcl \
--host human \
--sample-sheet /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/CellRanger_SampleSheet_NGS_0543.csv \
--design /data/RTB_GRS/ActiveProjects/NGS_0543_Singh/satya_atac_design.csv  \
--output /data/$USER/Test_Space/GRS_SC10X \
--mode slurm
# -------------------------------------------------------



