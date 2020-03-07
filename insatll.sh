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


while [ "$1" != "" ]; do
    case $1 in
        -t|--test) shift
                   HOME="$1"
                   echo "Test directory is : $HOME"
                   ;;

        * ) continue
    esac
    shift
done


# check script existence
if [[ -e "$HOME/.passman" ]]; then
    echo "You installed package already! CHECK : $HOME/.passman"
    exit
fi
# download script archive
echo "Downloading passman.zip"
curl -so passman.zip https://github.com/malijani/passwordmanager/raw/master/archive/passman.zip
unzip passman.zip
mv pasman/ $HOME/.passman
rm passman.zip
cd $HOME/.passman
# create .vev directory
virtualenv .venv -p python3
# add aliases for user shell
if [[ $(echo $SHELL | grep bash) ]] ;then
    if [[ ! $(grep "activenv" $HOME/.bashrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> $HOME/.bashrc
        echo "alias passman='cd  $HOME/.passman && activenv && ./passman.py'" >> $HOME/.bashrc
    else
        echo "Script is configured for you!"
    fi
elif [[ $(echo $SHELL | grep zsh) ]] ; then
    if [[ ! $(grep activenv $HOME/.zshrc) ]]; then
        echo -e "\nalias activenv='source .venv/bin/activate'" >> $HOME/.zshrc
        echo "alias passman='cd  $HOME/.passman && activenv && ./passman.py'" >> $HOME/.zshrc
    else
        echo "Script is configured for you!"
    fi
else
    echo "****Please add these lines to your .${SHELL}rc file and continue with manual installation****"
    echo "alias activenv='source .venv/bin/activate'"
    echo "alias passman='cd $HOME/.passman && activenv && ./passman.py'"
    exit
fi
# activate virtual environment for installing the needed libraries
source .venv/bin/activate
# install needed libraries for passwordmanager
pip3 install -r requirements.txt
# deactivate virtual environment
deactivate
# view the configured aliases
echo "run: 'passman --help' to see script help"
