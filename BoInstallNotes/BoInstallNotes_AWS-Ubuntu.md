
sudo apt update
sudo apt install software-properties-common apt-transport-https wget -y


#Install VSCode
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install code
code --version


#Install Git/Github
sudo apt install gh
gh auth login

sudo apt install nodejs
sudo apt install npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
nvm list-remote
nvm install v20.12.2
node -v

#Clone the Node repo
gh repo clone BCordleRossVideo/2024-BoRosstalkAPI
cd 2024-BoRosstalkAPI

#Clone the RealtimeSTT Repo
gh repo clone BCordleRossVideo/RealtimeSTT