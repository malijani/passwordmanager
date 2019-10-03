# ABOUT
**This script helps me to manage my PASSWORDs and encrypt them in place with sqlite3 database!
My secure way to protect password data!
You can add it to a live persistent system to have your system and passwords with yourself everywhere!
my way : a persistent encrypted kalilinux on a flash USB!**
# Download And Config
###### download:
```bash
mkdir -p ~/SourceVersionControl/github.com/virtualdemon && cd ~/SourceVersionControl/github.com/virtualdemon && git clone https://github.com/virtualdemon/passwordmanager
```
###### configure:
**USE .bashrc ALTERNATE FOR YOUR SHELL ; sample : ~/.zshrc
**
```bash
cd ~/SourceVersionControl/github.com/virtualdemon
pip install virtualenv
virtualenv .venv # python3
echo "alias activenv='source .venv/bin/activate'" >> ~/.bashrc
echo "alias passwordmanager='cd ~/SourceVersionControl/github.com/virtualdemon && activenv && ./passwordmanager.py'" >> ~/.bashrc
activenv
pip install -r requirements.txt
deactivate
cd $HOME
passwordmanager --help
```

# USAGE
```
usage: PASS STORE [-h] [--id ID] [--user_name USER_NAME]
                  [--website_address WEBSITE_ADDRESS]
                  [--phone_number PHONE_NUMBER] [--password PASSWORD]
                  [--length LENGTH] [--intractive] [--email EMAIL]
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
  --intractive          take data in intractive mode
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