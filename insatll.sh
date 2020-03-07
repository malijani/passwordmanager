#!/usr/bin/env bash

# check git, pip3, python3 installation
has() {
    if ! [ -x "$(command -v $1)" ]; then
        echo "Error: $1 is not installed. please install it first!" >&2
        exit 1
    fi
}
has pip3
has python3
has virtualenv
has unzip
has curl

# check script existence
if [[ -e "~/.passman" ]]; then
    echo "You installed package already! CHECK : ~/.passman"
    exit
fi
# download script archive
echo "Downloading passman.zip"
mkdir -p ~/.passman
cd ~/.passman

# create .vev directory
virtualenv .venv -p python3
# add aliases for user shell
if [[ $(echo $SHELL | grep bash) ]] ;then
    if [[ ! $(grep activenv ~/.bashrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> ~/.bashrc
        echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'" >> ~/.bashrc
        echo "alias update-passwordmanager='cd ~/.passwordmanager && curl -s -o passwordmanager.py https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/passwordmanager.py && curl -s -o requirements.txt https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/requirements.txt && activenv && pip3 install -r requirements.txt && deactivate && cd'" >> ~/.bashrc
    else
        echo "Script is configured for you!"
    fi
elif [[ $(echo $SHELL | grep zsh) ]] ; then
    if [[ ! $(grep activenv ~/.zshrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> ~/.zshrc
        echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'" >> ~/.zshrc
        echo "alias update-passwordmanager='cd ~/.passwordmanager && curl -s -o passwordmanager.py https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/passwordmanager.py && curl -s -o requirements.txt https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/requirements.txt && activenv && pip3 install -r requirements.txt && deactivate && cd'" >> ~/.zshrc
    else
        echo "Script is configured for you!"
    fi
else
    echo "****Please add these lines to your .${SHELL}rc file and continue with manual installation****"
    echo "alias activenv='source .venv/bin/activate'"
    echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'"
    echo "alias update-passwordmanager='cd ~/.passwordmanager && curl -s -o passwordmanager.py https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/passwordmanager.py && curl -s -o requirements.txt https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/requirements.txt && activenv && pip3 install -r requirements.txt && deactivate && cd'"
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
