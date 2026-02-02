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

### Environment Variables

```text
Libro-FM_account_user_#
Libro-FM_account_password_#
```

### Command Line

```text
-u OR --user 
-p OR --password 
```

## Bulk Account Ingest

Libro-Tea can ingest accounts in two ways:

1. **`accounts.json` file**
2. **Environment variables**

The application will:

1. Load accounts from `accounts.json` if present
2. Append any accounts found in environment variables

Docker Secrets are supported for environment variables.

---

## Configuration Settings

Configuration can be provided via **environment variables** or a **config file**.
All true or false options are set to false when using command line unless specified by the user.

### General Configuration Options

#### `Dry Run`

Creates the directory structure for all owned audiobooks across accounts without downloading files.

* **Config File key name:** `catalog_only`
* **Command Line Argument** `--dry-run`
* **Environment Variable:** `LIBRO-TEA_catalog_only`
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
* **Environment Variable:** `LIBRO-TEA_export_cover`
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
* **Environment Variable:** `LIBRO-TEA_export_metadata`
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
* **Environment Variable:** `LIBRO-TEA_export_cue`
* **Accepted Values:** `True`, `False`
* **Default:** `True`

---

#### `Force Download All audiobooks`

Always downloads audiobooks, even if they have been flagged as downloaded.
The audiobook must be owned by an account to be downloaded.

* **Config File key name:** `force_download`
* **Command Line Argument** `--download-all`
* **Environment Variable:** `LIBRO-TEA_force_download`
* **Accepted Values:** `True`, `False`
* **Default:** `False`

---

#### `Rename Audiobook Files to Title`

Enables and disables the renaming of downloaded audiobook files to the title of the audiobook.

* **Config File key name:** `rename_to_title`
* **Command Line Argument** `--rename-to-title`
* **Environment Variable:** `LIBRO-TEA_rename_to_title`
* **Accepted Values:** `True`
* **Default:** `False`

---

#### `M4B/MP3 Selection`

Sets the preferred audiobook output format.
Libro-Tea will attempt to download the preferred format but will fall back to what is available.

* **Config File key name:** `preferred_output`
* **Command Line Argument** `--pererred_output`
* **Environment Variable:** `LIBRO-TEA_prefered_output`
* **Accepted Values:** `M4B`, `MP3`
* **Default:** `M4B`

---

#### `Account.json Directory Path`

Specify the file path of the account.json file. 
If using command line, is used in conjunction with account.json directory path.

* **Config File key name:** `account_dir`
* **Command Line Argument** `--account`
* **Environment Variable:** `LIBRO-TEA_account_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Account.json File Name`

Specify the name of the account.json file. 
If using command line, is used in conjunction with account.json directory path.

* **Config File key name:** `account_file`
* **Command Line Argument** `--account`
* **Environment Variable:** `LIBRO-TEA_account_file`
* **Accepted Values:** `path/to/file.json`
* **Default:** `account.json`

---

#### `Config Directory Path`

Specify the file path of the config.json file.

* **Config File key name:** `config_dir`
* **Environment Variable:** `LIBRO-TEA_config_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Config File Name`

Specify the name of the config.json file. 

* **Config File key name:** `config_file`
* **Environment Variable:** `LIBRO-TEA_config_file`
* **Accepted Values:** `file.json`
* **Default:** `config.json`

---

#### `Database Directory`

Specify the file path of the database.db file. 
If using command line, is used in conjunction with database.db directory path.

* **Config File key name:** `database_dir`
* **Command Line Argument** `--database`
* **Environment Variable:** `LIBRO-TEA_database_dir`
* **Accepted Values:** `path/to/dir/`
* **Default:** `./`

---

#### `Database File Name`

Specify the name of the database.db file. 
If using command line, is used in conjunction with database.db directory path.

* **Config File key name:** `database_file`
* **Command Line Argument** `--database`
* **Environment Variable:** `LIBRO-TEA_database_file`
* **Accepted Values:** `file.db`
* **Default:** `library.db`

---

#### `Audiobook output directory`

Sets the output directory for audiobooks.

* **Config File key name:** `output_dir`
* **Command Line Argument** `--output-path`
* **Environment Variable:** `LIBRO-TEA_output_dir`
* **Accepted Values:** System paths
* **Default:** `./Audiobooks`

---

#### `Current Working Dir`

Sets the working directory for the program. This is were your config.son, account.json, and library.db are. Should be set in both the environment and config file (if being used). 

* **Config File key name:** `working_dir`
* **Environment Variable:** `LIBRO-TEA_working_dir`
* **Accepted Values:** System paths
* **Default:** `./`

---

#### `Debug Messages`

Displays additional system messages for debugging.

* **Config File key name:** `debug`
* **Command Line Argument** `-v`, `--debug` for basic, `-vv` for Verbose
* **Environment Variable:** `LIBRO-TEA_debug`
* **Accepted Values:**

  * `0` – Disabled (default)
  * `1` – Basic debug
  * `2` – Verbose debug

* **Default:** `0`

---

## To-Do

* Docker Container
* Reset audiobook download status
