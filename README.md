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

## Account Ingest

Libro-Tea can ingest accounts in two ways:

1. **`accounts.json` file**
2. **Environment variables**

The application will:

1. Load accounts from `accounts.json` if present
2. Append any accounts found in environment variables

Docker Secrets are supported for environment variables.

### Environment Variables

```text
Libro.FM_account_user_#
Libro.FM_account_password_#
```

---

## Configuration Settings

Configuration can be provided via **environment variables** or a **config file**.

### General Configuration Options

#### `Dry Run`

Creates the directory structure for all owned audiobooks across accounts without downloading files.

* **Config File key name:** `catalog_only`
* **Environment Variable:** `LIBRO-TEA_catalog_only`
* **Accepted Values:** `True`, `False` (default)

---

#### `Get Libro.FM Audiobook Cover`

Downloads cover art from Libro.fm and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_cover`
* **Environment Variable:** `LIBRO-TEA_export_cover`
* **Accepted Values:** `True` (default), `False`

---

#### `Export Audiobook Metadata`

Generates a `metadata.json` file for each audiobook and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_metadata`
* **Environment Variable:** `LIBRO-TEA_export_metadata`
* **Accepted Values:** `True` (default), `False`

---

#### `Get Audiobook CUE file`

Generates or exports a CUE file and places it in:

```text
./Audiobooks/<author>/<title>/
```

* **Config File key name:** `export_cue`
* **Environment Variable:** `LIBRO-TEA_export_cue`
* **Accepted Values:** `True` (default), `False`

---

#### `Download All audiobooks`

Always downloads audiobooks, even if they have been flagged as downloaded.
The audiobook must be owned by an account to be downloaded.

* **Config File key name:** `force_download`
* **Environment Variable:** `LIBRO-TEA_force_download`
* **Accepted Values:** `True`, `False` (default)

---

#### `M4b/MP3 Selection`

Sets the preferred audiobook output format.
Libro-Tea will attempt to download the preferred format but will fall back to what is available.

* **Config File key name:** `preferred_output`
* **Environment Variable:** `LIBRO-TEA_prefered_output`
* **Accepted Values:** `"M4B"` (default), `"mp3"`

---

#### `Audiobook output directory`

Sets the output directory for audiobooks.

* **Config File key name:** `output_dir`
* **Environment Variable:** `LIBRO-TEA_output_dir`
* **Accepted Values:** System paths
* **Default:** `./Audiobooks`

---

#### `Current Working Dir`

Sets the working directory for the program.

* **Config File key name:** `working_dir`
* **Environment Variable:** `LIBRO-TEA_working_dir`
* **Accepted Values:** System paths
* **Default:** `./`

---

#### `Debug Messages`

Displays additional system messages for debugging.

* **Config File key name:** `debug`
* **Environment Variable:** `LIBRO-TEA_debug`
* **Accepted Values:**

  * `0` – Disabled (default)
  * `1` – Basic debug
  * `2` – Verbose debug

---

## Required Python Modules

* `librofm`
* `requests`
* `mutagen`
* `pathlib`

---

##️ To-Do

* Add argument parsing
* Allow changing the working directory at runtime
* Support case-insensitive environment variables
* Reset audiobook download status
