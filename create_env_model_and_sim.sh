#! /bin/bash
set -e
source ~/anaconda3/etc/profile.d/conda.sh
NAME=Model_and_Sim
VERSION=3.9
DIR=~/Simulation
conda create -y -n $NAME python=$VERSION
conda activate $NAME

#
# install additional packages for linting and testing
pip install -U pip  
pip install pylint
pip install pycodestyle
pip install black

# git clone git@github.com:tomtuamnuq/model_and_simulate.git

pip install numpy
pip install matplotlib
pip install scipy
pip install pandas
pip install pygame

