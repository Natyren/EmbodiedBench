ARG CUDA_VERSION=11.4.3
ARG NVIDIA_VERSION=535.161.08

FROM nvidia/cuda:$CUDA_VERSION-devel-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends python3-pip libvulkan1 python3-venv vim pciutils wget git kmod vim bzip2 build-essential libffi-dev python3-dev libgtk2.0-dev


ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p ${CONDA_DIR} && \
    rm /tmp/miniconda.sh

ENV PATH=${CONDA_DIR}/bin:$PATH

# RUN git clone https://github.com/EmbodiedBench/EmbodiedBench.git /opt/embodiedbench
# syntax=docker/dockerfile:1.2
ARG GITHUB_USERNAME=Natyren
RUN --mount=type=secret,id=github_token \
    git clone https://${GITHUB_USERNAME}:$(cat /run/secrets/github_token)@github.com/EmbodiedBench/EmbodiedBench.git /opt/embodiedbench


WORKDIR /opt/embodiedbench


COPY scripts/install_nvidia.sh /app/
RUN NVIDIA_VERSION=$NVIDIA_VERSION /app/install_nvidia.sh

############################ 1. Setup Env for EB-Alf and EB-Hab ############################

RUN conda env create -f conda_envs/environment.yaml && conda clean --all -y

RUN conda run -n embench pip install -e .

# 1. Habitat-Sim and Habitat-Lab
RUN bash -c "source /opt/conda/etc/profile.d/conda.sh && \
             conda activate embench && \
             conda install -y habitat-sim==0.3.0 withbullet headless -c conda-forge -c aihabitat"
             
RUN bash -c "source /opt/conda/etc/profile.d/conda.sh && \
             conda activate embench && \
             git clone -b 'v0.3.0' --depth 1 https://github.com/facebookresearch/habitat-lab.git /root/habitat-lab"

RUN bash -c "source /opt/conda/etc/profile.d/conda.sh && \
             conda activate embench && \
             cd /root/habitat-lab && \
             pip install -e habitat-lab && \
             pip install -e habitat-baselines && \
             pip install numpy==1.23.5"

# 2. YCB and ReplicaCAD
RUN bash -c "source /opt/conda/etc/profile.d/conda.sh && \
             conda activate embench && \
             cd /opt/embodiedbench/embodiedbench/envs/eb_habitat && \
             conda install -y -c conda-forge git-lfs && \
             python -m habitat_sim.utils.datasets_download --uids rearrange_task_assets"


############################ 2. Setup Env for EB-Nav ############################

RUN conda env create -f conda_envs/environment_eb-nav.yaml && conda clean --all -y

RUN conda run -n embench_nav pip install -e .

CMD ["/bin/bash"]