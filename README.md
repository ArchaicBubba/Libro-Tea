# Libro-Tea

**Libro-Tea** allows you to download all audiobooks owned by one or more Libro.fm accounts and organize them into a clean, Audiobookshelf ready structure.

---

## Features

* Multi-account audiobook downloading
* Indexes audiobooks to prevent duplicate downloads
* Optional force-download of all owned audiobooks
* Downloads and stores cover art in the audiobook folder
* Automatically renames audiobooks to their title
* Exports audiobook metadata from Libro.fm and packages it for **Audiobookshelf**
* Supports downloading audiobooks as **MP3** or **M4B** (when available on Libro.fm servers)
* Generates CUE files from MP3 downloads or exports CUE data from M4B metadata
* Docker Secret support for account credentials

---

## Docker

```text

```

---

### Environment Variables

```text
LIBRO_FM_account_user_#
LIBRO_FM_account_password_#
```

### Command Line

```text
-u OR --user 
-p OR --password 
```

## Bulk Account Ingest

Libro-Tea can ingest accounts in two ways:

1. **`account.json` file**
2. **Environment variables**

The application will:

1. Load accounts from `account.json` if present
2. Append any accounts found in environment variables

Docker Secrets are supported for environment variables.

---

## Docker

Docker Compose example
```
services:
  libro-tea:
    image: archaicbubba/libro-tea:latest
    container_name: libro-tea
    restart: unless-stopped
    volumes:
      - path/to/your/config:/librotea/config
      - path/to/your/audiobook:/librotea/AudioBooks
    environment:
#     How often LIBRO TEA will check for new AudioBooks
      - LIBRO_TEA_second=0
      - LIBRO_TEA_min=30
      - LIBRO_TEA_hour=0
      - LIBRO_TEA_day=0
#     General application settings
#     - LIBRO_TEA_export_cover=True # Default True
#     - LIBRO_TEA_export_metadata=True # Default True
#     - LIBRO_TEA_export_cue=False # Default False
#     - LIBRO_TEA_prefered_output=M4B # Default MP4, Alt MP3 if avalible
#     - LIBRO_TEA_rename_to_title=True # Default True
#     - LIBRO_TEA_clear_working=True  # Default True
#     - LIBRO_TEA_debug=0 # values 0-2
#     User settings, Can be put here or in the account.json file in config. Libro_FM_account_user_n, Libro_FM_account_password_n for however many accounts that are being pulled
#      - LIBRO_FM_account_user_1=user@example.com
#      - LIBRO_FM_account_password_1=PaSSwoRd
#      - Libro_FM_account_user_2=/run/secrets/account_user_2
#      - Libro_FM_account_password_2=/run/secrets/account_password_2
#    secrets:
#      - account_user_2
#      - account_password_2

#Example Secrets
#secrets:
#  account_user_2:
#    file: ./example/docker-secrets/account_user_2.txt
#  account_password_2:
#    file: ./example/docker-secrets/account_password_2.txt
```

Building from source

```
git clone https://github.com/ArchaicBubba/Libro-Tea.git
cd Libro-Tea
docker build -t libro-tea .
```

Common Issues

+ Unable to write to dirctory. Solution: Change ownership to 1000. 
+ Access_Token required/missing. Solution: Incorrect Username and/or password

---

## Configuration Settings

Configuration can be provided via **environment variables** or a **config file**.
All true or false options are set to false when using command line unless specified by the user.

### General Configuration Options

#### `Dry Run`

Creates the directory structure for all owned audiobooks across accounts without downloading files.

* **Config File key name:** `catalog_only`
* **Command Line Argument** `--dry-run`
* **Environment Variable:** `LIBRO_TEA_catalog_only`
* **Accepted Values:** `True`, `False`
* **Default:** `False`

---

#### `Get Libro.FM Audiobook Cover`

Downloads cover art from Libro.fm and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_cover`
* **Command Line Argument** `--export-cover`
* **Environment Variable:** `LIBRO_TEA_export_cover`
* **Accepted Values:** `True`, `False`
* **Default:** `True`

---

#### `Export Audiobook Metadata`

Generates a `metadata.json` file for each audiobook and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_metadata`
* **Command Line Argument** `--export-metadata`
* **Environment Variable:** `LIBRO_TEA_export_metadata`
* **Accepted Values:** `True`, `False`
* **Default:** `True`

---

#### `Get Audiobook CUE file`

Generates or exports a CUE file and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_cue`
* **Command Line Argument** `--export-cue`
* **Environment Variable:** `LIBRO_TEA_export_cue`
* **Accepted Values:** `True`, `False`
* **Default:** `True`

---

#### `Force Download All audiobooks`

Always downloads audiobooks, even if they have been flagged as downloaded.
The audiobook must be owned by an account to be downloaded.

* **Config File key name:** `force_download`
* **Command Line Argument** `--download-all`
* **Environment Variable:** `LIBRO_TEA_force_download`
* **Accepted Values:** `True`, `False`
* **Default:** `False`

---

#### `Rename Audiobook Files to Title`

Enables and disables the renaming of downloaded audiobook files to the title of the audiobook.

* **Config File key name:** `rename_to_title`
* **Command Line Argument** `--rename-to-title`
* **Environment Variable:** `LIBRO_TEA_rename_to_title`
* **Accepted Values:** `True`, `False`
* **Default:** `False`

---

#### `Clear Working Dir`

Clears Temporary files on completion of program. This will DELETE the folder working folder that Libro-Tea creats. DO NOT SET this to a folder that you have data in.

* **Config File key name:** `clear_working`
  --keep-working-dir
* **Environment Variable:** `LIBRO_TEA_clear_working`
* **Accepted Values:** `True`, `False`
* **Default:** `True`

---

#### `M4B/MP3 Selection`

Sets the preferred audiobook output format.
Libro-Tea will attempt to download the preferred format but will fall back to what is available.

* **Config File key name:** `preferred_output`
* **Command Line Argument** `--pererred_output`
* **Environment Variable:** `LIBRO_TEA_prefered_output`
* **Accepted Values:** `M4B`, `MP3`
* **Default:** `M4B`

---

#### `Account.json Directory Path`

Specify the file path of the account.json file.
If using command line, is used in conjunction with account.json directory path.

* **Config File key name:** `account_dir`
* **Command Line Argument** `--account`
* **Environment Variable:** `LIBRO_TEA_account_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Account.json File Name`

Specify the name of the account.json file.
If using command line, is used in conjunction with account.json directory path.

* **Config File key name:** `account_file`
* **Command Line Argument** `--account`
* **Environment Variable:** `LIBRO_TEA_account_file`
* **Accepted Values:** `path/to/file.json`
* **Default:** `account.json`

---

#### `Config Directory Path`

Specify the file path of the config.json file.

* **Config File key name:** `config_dir`
* **Environment Variable:** `LIBRO_TEA_config_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Config File Name`

Specify the name of the config.json file.

* **Config File key name:** `config_file`
* **Environment Variable:** `LIBRO_TEA_config_file`
* **Accepted Values:** `file.json`
* **Default:** `config.json`

---

#### `Database Directory`

Specify the file path of the database.db file.
If using command line, is used in conjunction with database.db directory path.

* **Config File key name:** `database_dir`
* **Command Line Argument** `--database`
* **Environment Variable:** `LIBRO_TEA_database_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Database File Name`

Specify the name of the database.db file.
If using command line, is used in conjunction with database.db directory path.

* **Config File key name:** `database_file`
* **Command Line Argument** `--database`
* **Environment Variable:** `LIBRO_TEA_database_file`
* **Accepted Values:** `file.db`
* **Default:** `library.db`

---

#### `Audiobook output directory`

Sets the output directory for audiobooks.

* **Config File key name:** `output_dir`
* **Command Line Argument** `--output-path`
* **Environment Variable:** `LIBRO_TEA_output_dir`
* **Accepted Values:** System paths
* **Default:** `./Audiobooks`

---

#### `Current Working Dir`

Sets the working directory for the program. This is were your config.json, account.json, and library.db are. Should be set in both the environment and config file (if being used).

* **Config File key name:** `working_dir`
* **Environment Variable:** `LIBRO_TEA_working_dir`
* **Accepted Values:** System paths
* **Default:** `./`

---

#### `Debug Messages`

Displays additional system messages for debugging.

* **Config File key name:** `debug`
* **Command Line Argument** `-v`, `--debug` for basic, `-vv` for Verbose
* **Environment Variable:** `LIBRO_TEA_debug`
* **Accepted Values:**

  * `0` – Disabled (default)
  * `1` – Basic debug
  * `2` – Verbose debug
* **Default:** `0`

---

## To-Do

* Reset audiobook download status
