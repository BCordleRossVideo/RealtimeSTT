So, it works, but it's slow. 

python3 tests/realtimestt_test.py

It's not real slow, but too slow to use to cut cameras for a production.

Sequence of commands I used to configure my WSL2 setup on a 2RU XPN Chassis w/ NVIDIA GPU

wsl --install -d ubuntu

sudo apt update
sudo apt upgrade
sudo apt install python3-pip
python3 -m pip install --upgrade pip setuptools wheel

nano ~/.bashrc
Add to end of file:
export PATH="$HOME/.local/bin:$PATH"
To Restart:
source ~/.bashrc

sudo apt install gh
gh auth login

gh repo clone KoljaB/RealtimeSTT

sudo apt install python3-venv
cd RealtimeSTT/
python3 -m venv realtimestt.venv
source realtimestt.venv/bin/activate

sudo apt-get update
sudo apt-get install portaudio19-dev
pip install pyaudio
pip install RealtimeSTT

sudo apt install pulseaudio
pulseaudio --start

[Running tests/simple_test.py had a file not found error for cudnn8 or something]

wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run

sudo sh cuda_11.8.0_520.61.05_linux.run
(accept, install)
sudo sh cuda_11.8.0_520.61.05_linux.run --silent --driver

nano ~/.bashrc
Add to end of file:
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH

To Restart:
source ~/.bashrc

[download and transver cudnn file]
sudo dpkg -i cudnn-local-repo-ubuntu2204-8.7.0.84_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2204-8.7.0.84/cudnn-local-BF23AD8A-keyring.gpg /usr/share/keyrings/

(still getting error:
Could not load library libcudnn_ops_infer.so.8. Error: libcudnn_ops_infer.so.8: cannot open shared object file: No such file or directory
Aborted)

Throwing a bunch of stuff at the wall...

sudo apt install nvidia-cuda-toolkit
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get install libcudnn8
sudo apt-get install libcudnn8-dev

It works!!

sudo apt update && sudo apt install ffmpeg

