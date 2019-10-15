# ABOUT
**This script helps me to manage my PASSWORDs and encrypt them in place with sqlite3 database!**

**My secure way to protect password data!**

**You can add it to a live persistent system to have your system and passwords with yourself everywhere!**

my way : **a persistent encrypted kalilinux on a flash USB!**

<!---[![asciicast](https://asciinema.org/a/e38VtPgyLQZWyZjURTbtWrgUt.png)](https://asciinema.org/a/e38VtPgyLQZWyZjURTbtWrgUt) --->


![RepoSize](https://img.shields.io/github/repo-size/virtualdemon/passwordmanager.svg?style=flat-square) ![Contributors](https://img.shields.io/github/contributors/virtualdemon/passwordmanager.svg?style=flat-square)

# Download, Config And Update

## Automated installation (supports bash, zsh):
```bash
curl -s https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/install-and-configure.sh | bash
```

## Manual installation:

###### download:
```bash
mkdir -p ~/.passwordmanager
cd ~/.passwordmanager
curl -s -o passwordmanager.py https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/passwordmanager.py
chmod +x passwordmanager.py
curl -s -o requirements.txt https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/requirements.txt
```

###### configure:
**USE .bashrc ALTERNATE FOR YOUR SHELL ; sample : ~/.zshrc**

```bash
cd ~/.passwordmanager
pip install virtualenv
virtualenv .venv -p python3
echo "alias activenv='source .venv/bin/activate'" >> ~/.bashrc
echo "alias passwordmanager='cd ~/.passwordmanager && activenv && ./passwordmanager.py'" >> ~/.bashrc
activenv
pip install -r requirements.txt
deactivate
cd $HOME
passwordmanager --help
```

after using the script just rund `deactivate` command to disable virtual environment!

##### update:
```bash
echo "alias update-passwordmanager='cd ~/.passwordmanager && curl -s -o passwordmanager.py https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/passwordmanager.py
 && curl -s -o requirements.txt https://raw.githubusercontent.com/virtualdemon/passwordmanager/master/requirements.txt && activenv && pip3 install -r requirements.txt && deactivate && cd'" >> ~/.bashrc
update-passwordmanager
```

# USAGE

set a unique key to encrypt and decrypt your passwords in database! just run script with this (KEY):>

```
usage: PASS STORE [-h] [--id ID] [--user_name USER_NAME]
                  [--website_address WEBSITE_ADDRESS]
                  [--phone_number PHONE_NUMBER] [--password PASSWORD]
                  [--length LENGTH] [--email EMAIL]
                  [--description DESCRIPTION] [--delete] [--update]
                  [--show_content] [--show_enc_content] [--insert]
                  [--table_name TABLE_NAME] [--database DATABASE]
                  [--column COLUMN] [--get_tables] [--search SEARCH]

passwordmanager is a programm to manage password database

optional arguments:
  -h, --help            show this help message and exit
  --id ID               table id for process
  --user_name USER_NAME
                        set user name
  --website_address WEBSITE_ADDRESS
                        websiteaddress
  --phone_number PHONE_NUMBER
                        set phone number
  --password PASSWORD   user "GEN" to generate password or set your custom
                        password
  --length LENGTH       set password length for auto-generation
  --email EMAIL         set acc email
  --description DESCRIPTION
                        set field description
  --delete              delete a specific row
  --update              change data in row
  --show_content        show table
  --show_enc_content    show enc table
  --insert              create a new row
  --table_name TABLE_NAME
                        table name
  --database DATABASE   database address
  --column COLUMN       input column
  --get_tables          get tablenames in database
  --search SEARCH       search in table with website address
```