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
has wget

# check script existence
if [[ -e "$HOME/.passman" ]]; then
    echo "You installed package already! CHECK : $HOME/.passman"
    exit
fi
# download script archive
echo "Downloading passman.zip"
# download script archive
wget passman.zip https://github.com/malijani/passwordmanager/raw/master/archive/passman.zip
# unzip passman.zip
unzip passman.zip
# move passman to HOME/.passman
mv passman/ $HOME/.passman
# remove passman.zip
rm passman.zip
# change directory to .passman
cd $HOME/.passman
# create .vev directory
command virtualenv -p python3 .venv
# activate virtual environment for installing the needed libraries
source ./.venv/bin/activate
# install needed libraries for passman
pip3 install -r requirements.txt
# deactivate virtual environment
deactivate

# change directory to HOME
cd $HOME

# show .passman directory
ls -R .passman

cat <<EOF
"PLEASE ADD THIS FUNCTION TO YOUR ~/.bashrc or ~/.shell*rc file!"

passman() {
    wd=\$(pwd)
    cd ~/.passman
    source .venv/bin/activate
    ./passman.py "\$@"
    deactivate
    cd "\$wd";
}

EOF

# view the configured aliases
echo "After adding function you can run: 'passman --help' to see script help and use it!"
