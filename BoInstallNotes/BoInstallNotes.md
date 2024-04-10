For a new WSL2 installation, follow the following:

chmod +x setup.sh
./setup.sh

Setup Python Virtual Environment:

cd RealtimeSTT/
python3 -m venv realtimestt.venv
source realtimestt.venv/bin/activate
pip install -r requirements.txt