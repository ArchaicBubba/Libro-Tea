import libraryManagment, settings, metadata
import zipfile, os
from librofm.client import LibroFMClient
from librofm.util import clean_filename
from pathlib import Path

# main downloads audiobooks function
def download_audiobook(audiobook, client):
    # Identifes and makes audiobook path. 
    authors = Path(clean_filename(', '.join(audiobook.authors)))
    title = Path(clean_filename(audiobook.title))
    path = settings.config["output_dir"] / authors / title
    path.mkdir(parents=True, exist_ok=True)
    # In try catch in case download failes, wont kill eithire 
    try:
        if settings.config["prefered_output"].lower()=="mp3":
            print(f"SYS MES - RUNNING - Starting {audiobook.title} download in MP3; please wait.")
            attempt = client.download_mp3(audiobook, path)
            extract_zip(path)
        elif settings.config["prefered_output"].lower()=="m4b":
            print(f"SYS MES - RUNNING - Starting {audiobook.title} download in M4B; please wait.")
            attempt = client.download_m4b(audiobook, path)
        else: # IF not specified by user, it will attempt both
            print(f"SYS MES - RUNNING - Starting {audiobook.title} Download please wait.")
            attempt = client.download(audiobook, path)
        if not attempt:
            # Additonal success check before modifying database
            print(f"SYS MES -  ERROR  - Failed to download {audiobook.title}")
            return
        # Changes audiobook status in database
        metadata.rename_to_title(audiobook.title, path)
        libraryManagment.set_book_downloaded(audiobook.isbn)
    except Exception as e:
        print(f"SYS MES -  ERROR  - Error downloading {audiobook.title}: {e}")
        return
    # Checks and gets cover for audiobook if wanted
    if settings.config["export_cover"]==True:
        metadata.export_cover(audiobook, path)
    # Checks and gets metadata for audiobook if wanted
    if settings.config["export_metadata"]==True:
        metadata.export_metadata(audiobook, path)
    # checks and makes Cue files if wanted
    if settings.config["export_cue"]==True:
        metadata.export_cue(audiobook, path)
    return

# Decides weather to download audiobook based off of library database. If audiobook is "New" it will be downloaded. 
# Audiobooks are stored in database as ISBNs, if multuple accounts own the same book it will only be downloaded once. 
def download_only_new(accounts):
    for account in accounts.values():
        # in try Catch to check if account credentials are valid, if not it wont kill the program and will try the next account if present.
        try:
            client = LibroFMClient(account["email"],account["password"])
            page = client.get_library()
            # Checks and downloads each new audiobook in the account. 
            for audiobook in page.audiobooks:                        
                if not libraryManagment.check_book_exists(audiobook.isbn):
                    libraryManagment.add_book(audiobook.isbn, audiobook.title)
                    download_audiobook(audiobook, client)
                    continue
                else:
                    if libraryManagment.is_book_downloaded(audiobook.isbn):
                        continue
                download_audiobook(audiobook, client)
        except Exception as e:
            print(f"SYS MES -  ERROR  - {e}")
            return

# Force Redownload of all Audiobooks, Still sets audiobooks as downloaded in database. 
def force_download_all(accounts):
    if not settings.config["force_download"]:
        return
    for account in accounts.values():
        # in try Catch to check if account credentials are valid, if not it wont kill the program and will try the next account if present.
        try:
            client = LibroFMClient(account["email"],account["password"])
            page = client.get_library()
            for audiobook in page.audiobooks:
                download_audiobook(audiobook, client)
        except Exception as e:
            print(f"SYS MES -  ERROR  - {e}")
            return

# only catalogs Audiobooks for a dry run
def catalog(accounts):
    if not settings.config["catalog_only"]:
        return
    for account in accounts.values():
        # in try Catch to check if account credentials are valid, if not it wont kill the program and will try the next account if present.
        try:
            client = LibroFMClient(account["email"],account["password"])
            page = client.get_library()
            for audiobook in page.audiobooks:
                authors = Path(clean_filename(', '.join(audiobook.authors)))
                title = Path(clean_filename(audiobook.title))
                path = settings.config["output_dir"] / authors / title
                path.mkdir(parents=True, exist_ok=True)
                if not libraryManagment.check_book_exists(audiobook.isbn):
                    libraryManagment.add_book(audiobook.isbn, audiobook.title)
                else:
                    continue
        except Exception as e:
            print(f"SYS MES -  ERROR  - {e}")
            return

# extracts downloaded zip file from libro office
def extract_zip(path):
    zipFiles = []
    for file in os.listdir(path):
        if file[-4:].lower()==".zip":
            zipFiles.append(file)
    for file in zipFiles:
        print(f"SYS MES - RUNNING - Extracting {path}/{file}")
        with zipfile.ZipFile(f"{path}/{file}") as zf:
            zf.extractall(path)
        os.remove(f"{path}/{file}")
    return