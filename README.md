# Libro-Tea
Allow you to download all Libro.FM audiobooks owned by one or multiple accounts.

# Feathers 
 - Multi-Account audiobook download
 - Indexes audiobooks so they arnt downloaded multiple times.
 - optional force download all.
 - Gets Cover and places it in the Audiobooks folder
 - Autoimaticly renames the audiobook to its title
 - Exports Audiobooks metadata from Libro.FM and packages it for Audiobookshelf. Places file in audiobook folder.
 - Allows user to choose to download mp3 or m4b formated audiobooks; if availble on Libro.FM servers.
 - Generates CUE file from the downloaded mp3 files or exports the cue file from the m4b's metadata.
 - Docker Secret support on account credetioals 

# Account Ingest
It can ingest accounts in two ways, though enviornment variables and an "accounts.json" file. Libro-Tea will first look for the json, then add any environment variables found. Docker Secrets are supported for environment variables.
- Libro.FM_account_user_#
- Libro.FM_account_password_#

# Configuration
Configuration can either be taken from the enviroment or from a config file. General config file settings are as follows:
 - catalog_only
     Makes file structure for all owned audiobooks accross accounts.
     Environment Variable: LIBRO-TEA_catalog_only
     Accepted Values: True, False (default)
 - export_cover
     Downloads the cover art from LibroFM. Places it in ./Audiobooks/"author"/"title" folder.
     Environment Variable: LIBRO-TEA_export_cover
     Accepted Values: True (default), False
 - export_metadata
     Genorates a metadata.json file for the audiobook. Places it in audiobook/"author"/"title" folder.
     Environment Variable: LIBRO-TEA_export_metadata
     Accepted Values: True (default), False
 - export_cue
     Genorates or exports a cue file, Places it in ./Audiobooks/"author"/"title" folder.
     Environment Variable: LIBRO-TEA_export_cue
     Accepted Values: True (default), False
 - force_download
     Will always download an audiobook regardless if it has already been downloaded. Book needs to be owned by the account.
     Environment Variable: LIBRO-TEA_force_download
     Accepted Values: True, False (default)
 - prefered_output
     Sets prefred audiobook output format. This will attempt to get the prefered format; but will get what is availble.
     Environment Variable: LIBRO-TEA_prefered_output
     Accepted Values: "M4B" (default), "mp3"
 - output_dir
     Sets output directores for Audiobooks
     Environment Variable: LIBRO-TEA_output_dir
     Accepted Values: System paths; "./Audiobooks" (default)
 - working_dir
     Sets working directory for program
     Environment Variable: LIBRO-TEA_working_dir
     Accepted Values: System Paths; "./" (default)
 - debug
     Displays more system messages to show where the program is running.
     Environment Variable: LIBRO-TEA_debug
     Accepted Values: 0 (default), 1, 2 (highest)

# Required python modules
 - librofm
 - requests
 - mutagen
 - pathlib

# to-do
- Argument Parsing
- change working directory.
- environment varibale caseincesitivity. 
- reset audiobook status.
