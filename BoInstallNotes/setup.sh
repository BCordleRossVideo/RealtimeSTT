#!/bin/bash

# Install Ubuntu on WSL2
wsl --install -d ubuntu

# System update and upgrade
sudo apt update
sudo apt upgrade -y

# Install Python3 pip and venv
sudo apt install python3-pip python3-venv -y

# Upgrade pip, setuptools, and wheel
python3 -m pip install --upgrade pip setuptools wheel

# Configure PATH in .bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Install GitHub CLI and authenticate
sudo apt install gh -y
gh auth login

# Clone RealtimeSTT repo
gh repo clone KoljaB/RealtimeSTT

# Install audio and CUDA dependencies
sudo apt-get install portaudio19-dev pulseaudio nvidia-cuda-toolkit -y
pulseaudio --start

# Download and install CUDA
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run --silent --driver

# Add CUDA to PATH and LD_LIBRARY_PATH
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc

# Install libcudnn
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get install libcudnn8 libcudnn8-dev -y

# Install ffmpeg
sudo apt update && sudo apt install ffmpeg -y

# Apply changes to .bashrc
source ~/.bashrc

echo "System setup complete. Please manually activate the RealtimeSTT virtual environment."
