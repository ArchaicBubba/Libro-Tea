# Libro-Tea
Allow you to download all Libro.FM audiobooks owned by one or multiple accounts.

# Account Ingest

# Configuration
Configuration can either be taken from the enviroment or from a config file. General config file settings are as follows:
 - catalog_only
     Makes file structure for all owned audiobooks accross accounts.
     Accepted Values: True, False (default)
 - export_cover
     Downloads the cover art from LibroFM. Places it in audiobook/"author"/"title" folder
     Accepted Values: True (default), False
 - export_metadata
     Genorates a metadata.json file for the audiobook. Places it in audiobook/"author"/"title" folder.
     Accepted Values: True (default), False
 - export_cue
     Genorates or exports a cue file, Places it in audiobook/"author"/"title" folder.
     Accepted Values: True (default), False
 - force_download
     Will always download an audiobook regardless if it has already been downloaded. Book needs to be owned by the account.
     Accepted Values: True, False (default)
 - prefered_output
     Sets prefred audiobook output format. This will attempt to get the prefered format; but will get what is availble.
     Accepted Values: "M4B" (default), "mp3"
 - output_dir
     Sets output directores for Audiobooks
     Accepted Values: System paths; "./Audiobooks" (default)
 - working_dir
     Sets working directory for program
     Accepted Values: System Paths; "./" (default)
 - debug
     Displays more system messages to show where the program is running.
     Accepted Values: 0 (default), 1, 2 (highest)

# Required python modules
 - librofm
 - requests
 - mutagen
 - pathlib
