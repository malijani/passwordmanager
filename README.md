# PASSMAN

![RepoSize](https://img.shields.io/github/repo-size/malijani/passwordmanager.svg?style=flat-square) ![Contributors](https://img.shields.io/github/contributors/malijani/passwordmanager.svg?style=flat-square)

## ABOUT

**Managing PASSWORDs and ENCRYPT them in place with cryptography!**

**You can install it on a live persistent system to have your system and passwords with yourself anywhere!**

> my way : **a persistent encrypted kali linux on a flash USB!**

# DEMO

[![asciicast](https://asciinema.org/a/25QiaZ8U5WInmT4rjkuyT7JXq.png)](https://asciinema.org/a/25QiaZ8U5WInmT4rjkuyT7JXq)


## INSTALL

You can simply run this command to download package and install it:

`curl https://raw.githubusercontent.com/malijani/passwordmanager/master/install.sh | bash`

then add this function to your ~/.bashrc (or ~/.shell*rc if you're using another kind of shell!):

```bash
passman() {
    wd=$(pwd)
    cd ~/.passman
    source .venv/bin/activate
    ./passman.py "$@"
    deactivate
    cd "$wd";
}
```

after adding this function you can use it :

`passman --help`

## USAGE

Set an unique key to to crypt passwords in database!

```
usage: passman [-h] [--id ID] [--website_address WEBSITE_ADDRESS]
               [--user_name USER_NAME] [--password PASSWORD] [--length LENGTH]
               [--email EMAIL] [--phone_number PHONE_NUMBER]
               [--description DESCRIPTION] [--insert] [--show_content]
               [--show_enc_content] [--search SEARCH] [--update] [--delete]
               [--table_name TABLE_NAME] [--database DATABASE] [--get_tables]

passman is a tool to manage your passwords safely

optional arguments:
  -h, --help            show this help message and exit
  --id ID               row id for process
  --website_address WEBSITE_ADDRESS
                        set website address
  --user_name USER_NAME
                        set user name
  --password PASSWORD   Set your custom password or "show" to show a generated
                        password or use "gen" to generate password directly
  --length LENGTH       set password length for auto-generation
  --email EMAIL         set acc email
  --phone_number PHONE_NUMBER
                        set phone number
  --description DESCRIPTION
                        set acc description
  --insert              create a new row
  --show_content        show decrypted data
  --show_enc_content    show encrypted data
  --search SEARCH       search in table with given argument
  --update              change data
  --delete              delete a specific row
  --table_name TABLE_NAME
                        set table name
  --database DATABASE   set database
  --get_tables          get table names in database
```
