# ABOUT
**This script helps me to manage my PASSWORDs and encrypt them in place with sqlite3 database!**

**My secure way to protect password data!**

**You can add it to a live persistent system to have your system and passwords with yourself everywhere!**

my way : **a persistent encrypted kalilinux on a flash USB!**

[![asciicast](https://asciinema.org/a/25QiaZ8U5WInmT4rjkuyT7JXq.png)](https://asciinema.org/a/25QiaZ8U5WInmT4rjkuyT7JXq)


![RepoSize](https://img.shields.io/github/repo-size/malijani/passwordmanager.svg?style=flat-square) ![Contributors](https://img.shields.io/github/contributors/malijani/passwordmanager.svg?style=flat-square)

# INSTALL

You can simply run this command to download package and install it:

`curl https://raw.githubusercontent.com/malijani/passwordmanager/master/install.sh | bash`

then add this function to your ~/.bashrc (or ~/.shell*rc if you're using another kind of shell!):

```passman() {
    wd=\$(pwd)
    cd ~/.passman
    source .venv/bin/activate
    ./passman.py "\$@"
    deactivate
    cd "\$wd";
}```

after adding this function you can use it :

`passman --help`

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
