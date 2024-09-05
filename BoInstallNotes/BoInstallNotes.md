For a new WSL2 installation, follow the following:

chmod +x setup.sh
./setup.sh

Setup Python Virtual Environment:

cd RealtimeSTT/
python3 -m venv realtimestt.venv
source realtimestt.venv/bin/activate
pip install -r requirements.txt



-----------------------------------------------------------

Probably not needed...

If you need to forward ports to WSL2 from LAN, use these commands from elevated Powershell on the host windows computer, not within wsl2.

C:\Users\XPression> netsh advfirewall firewall add rule name="Allowing LAN connections" dir=in action=allow protocol=TCP localport=9001
Ok.

C:\Users\XPression> netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9001 connectaddress=localhost connectport=9001


Had a lot of issues with program not using GPY. Created a gpu-test.py to confirm. Ended up being a versioning issue with torch and torchaudio. Needed v2.2.2+cu118

--------

8/22/24
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
python .\BoCode\Bo-GPU-Test.py
GPU is available.
NVIDIA GeForce GTX 1060

pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu125