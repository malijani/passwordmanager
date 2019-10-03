#!/usr/bin/env bash
# check git, pip3, python3 installation
if [[ ! $(which git) ]]; then
    echo "Please install git"
    exit
fi
if [[ ! $(which pip3) ]]; then
    echo "Please install python3-pip"
    exit
fi
if [[ ! $(which python3) ]]; then
    echo "Please install python3"
fi
# check script existence
if [[ -e "~/.passwordmanager" ]]; then
    echo "local repository already exist!: ~/.passwordmanager"
    exit
fi
# download script repository
echo "Downloading repository"
git clone https://github.com/virtualdemon/passwordmanager ~/.passwordmanager
cd ~/.passwordmanager
# install virtualenv with pip3
pip3 install virtualenv --user
# create .vev directory
virtualenv .venv -p python3
# add aliases for user shell
if [[ $(echo $SHELL | grep bash) ]] ;then
    if [[ ! $(grep activenv ~/.bashrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> ~/.bashrc
        echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'" >> ~/.bashrc
        echo "alias update-passwordmanager='cd ~/.passwordmanager && git pull -f && cd'" >> ~/.bashrc
    else
        echo "Script is configured for you!"
    fi
elif [[ $(echo $SHELL | grep zsh) ]] ; then
    if [[ ! $(grep activenv ~/.zshrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> ~/.zshrc
        echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'" >> ~/.zshrc
        echo "alias update-passwordmanager='cd ~/.passwordmanager && git pull -f && cd'" >> ~/.zshrc
    else
        echo "Script is configured for you!"
    fi
else
    echo "****Please add these lines to your .${SHELL}rc file and continue with manual installation****"
    echo "alias activenv='source .venv/bin/activate'"
    echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'"
    echo "alias update-passwordmanager='cd ~/.passwordmanager && git pull -f && cd'"
    exit
fi
# activate virtual environment for installing the needed libraries
source .venv/bin/activate
# install needed libraries for passwordmanager
pip3 install -r requirements.txt
# deactivate virtual environment
deactivate
# view the configured aliases
echo "run: 'passwordmanager --help' to see script help"
echo "run: 'update-passwordmanager' to update script"

