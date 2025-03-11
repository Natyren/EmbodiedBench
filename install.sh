#!/bin/bash

source "$(conda info --base)/etc/profile.d/conda.sh"
export EMBODIED_BENCH_ROOT=$(pwd)

conda init 
source ~/.bashrc

# # Environment for ```Habitat and Alfred```
conda env create -f conda_envs/environment.yaml 
conda activate embench
pip install -e .

# Environment for ```EB-Navigation```
conda env create -f conda_envs/environment_eb-nav.yaml 
conda activate embench_nav
pip install -e .

# Install Git LFS
git lfs install
git lfs pull

# Install EB-ALFRED
conda activate embench
git clone https://huggingface.co/datasets/EmbodiedBench/EB-ALFRED
mv EB-ALFRED embodiedbench/envs/eb_alfred/data/json_2.1.0

# Install EB-Habitat
conda activate embench
conda install -y habitat-sim==0.3.0 withbullet  headless -c conda-forge -c aihabitat
git clone -b 'v0.3.0' --depth 1 https://github.com/facebookresearch/habitat-lab.git ./habitat-lab
cd ./habitat-lab
pip install -e habitat-lab
cd ..
conda install -y -c conda-forge git-lfs
python -m habitat_sim.utils.datasets_download --uids rearrange_task_assets
mv data embodiedbench/envs/eb_habitat
