from . import account, libraryManagment, settings
from librofm.client import LibroFMClient
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
import os, json, requests, datetime, math

# Downloads the cover from LibroFM. Saves in audiobook folder.
def export_cover(title: str, coverURL:str, path:str) -> bool:
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - Starting cover download for \"{title}\", file path will be \"{path}/cover.jpg.\"")

    fullURL = f"https:{coverURL}"
    response = requests.get(fullURL)

    if response.status_code == 200:
        with open(f"{path}/cover.jpg", "wb") as f:
            f.write(response.content)
        if settings.config["debug"]>=1:
            print(f"DEBUG 1 - SUCCESS - Cover for \"{title}\" downloaded!")
        return True
    
    else:
        print(f"SYS MES -  ERROR  - Unable to find \"{title}\"'s cover")
        return False

# creates a metadata Json for audiobookshelf. Saves in audiobook folder
def export_metadata(audiobook: dict, path: str) -> bool:
    if settings.config["debug"]>=1:
        print(f"Debug 1 - RUNNING - Exporting Metadata for {audiobook.title}")

    # Stops if it cant find the specified book
    if not os.path.exists(path):
        if settings.config["debug"]>=1:
            print(f"Debug 1 - ERROR - Unable to export metadata for \"{audiobook.title}\"; file path \"{path}\" does not exist!")
        return False

    # Gets Genres
    genres = []
    for id in audiobook.genres:
        genres.append(id["name"])

    # Checks if it apart of a series
    if audiobook.series is not None:
        if audiobook.series_num is not None:
            series = str(audiobook.series + " #" + audiobook.series_num)
        else:
            series = audiobook.series
    else:
        series = None

    # generates Cue/chapter times for audiobookshelf
    chapters = generate_cue_for_metadata(audiobook.title, path)

    # Applys everything to an Audiobookshelf metadata dictionary 
    metadata = {
        "title": audiobook.title,
        "subtitle": audiobook.subtitle,
        "authors": audiobook.authors,
        "narrators": audiobook.audiobook_info["narrators"],
        "series": series,
        "genres": genres,
        "tags": audiobook.user_metadata["tags"],
        "publishedYear": str(audiobook.publication_date.year),
        "publishedDate": str(audiobook.publication_date),
        "publisher": audiobook.publisher,
        "description": audiobook.description,
        "isbn": audiobook.isbn,
        "asin": None,
        "language": audiobook.audiobook_info["audio_language_display"],
        "explicit": False,
        "abridged": audiobook.abridged,
        "chapters": chapters
    }

    # Exports above dictionary
    with open(f"{path}/metadata.json", "w") as f:
        f.write(json.dumps(metadata, indent=2))

    if settings.config["debug"]>=1:
        print(f"Debug 1 - SUCCESS - Finished Metadata for \"{audiobook.title}\"")
    return True

# Changes mp3/m4b files names to their book names
def rename_to_title(title: str, ignoredFiles: list, path: str) -> bool:
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - RUNNING - Renaming audiobook files for \"{title}\"")

    bookFiles = enumerate_audiobook_folder(path)

    for file in bookFiles:
        if file in ignoredFiles:
            bookFiles.remove(file)

    if bookFiles:
        if len(bookFiles)>1:
            bookFiles.sort()

            for i, file in enumerate(bookFiles):

                fileName, fileExt = os.path.splitext(file)
                if settings.config["debug"]>=1:
                    print(f"DEBUG 1 - RUNNING - Renaming \"{file}\" to \"{title} - part {i + 1 :03d}{fileExt}\"")
                os.rename(f"{path}/{file}", f"{path}/{title} - part {i + 1:03d}{fileExt}")

        elif len(bookFiles)==1: 
            fileName, fileExt = os.path.splitext(bookFiles[0])
            if settings.config["debug"]>=1:
                print(f"DEBUG 1 - RUNNING - Renaming \"{bookFiles[0]}\" to \"{title}{fileExt}\"")
            os.rename(f"{path}/{bookFiles[0]}", f"{path}/{title}{fileExt}")
        
        if settings.config["debug"]>=1:
            print(f"DEBUG 1 - SUCCESS - Finished renaming audiobook files for \"{title}\"")
        return True

    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - FAILURE - Unable to rename audiobook files for \"{title}\"")
    return False

# generates the cue file from the mp3s track length
def generate_cue_from_file(title: str, path: str) -> bool:
    if settings.config["debug"]>=1:
        print(f"Debug 1 - RUNNING - Generating cue for \"{title}\"")
    
    bookFiles = enumerate_audiobook_folder(path)

    if bookFiles:
        bookFiles.sort()

        with open(f"{path}/{title}.cue", "w") as f:
            totalTime = 0
            f.write("REM Source: LibroFM generated with Libro-Tea\n")
            f.write(f"TITLE \"{title}\"\n")

            for i, file in enumerate(bookFiles):
                fileName, fileExt = os.path.splitext(file)
                f.write(f"FILE \"{file}\"\n")

                if fileExt.lower()==".mp3":
                    mp3 = MP3(f"{path}/{file}")
                    f.write(f"  TRACK {i} AUDIO\n    TITLE \"{fileName}\"\n    INDEX 01 00:00:00\n")

                if fileExt.lower()==".m4b":
                    m4b = MP4(f"{path}/{file}")

                    for n, chapter in enumerate(m4b.chapters):
                        time = cue_time(chapter.start)
                        f.write(f"  TRACK {n :03d} AUDIO\n    TITLE \"{chapter.title}\"\n    INDEX 01 {time["minutes"] :02d}:{time["seconds"] :02d}:{time["frames"] :5.3f}\n")

            if settings.config["debug"]>=1:
                print(f"Debug 1 - SUCCESS - Generated cue for \"{title}\"")
            return True
    if settings.config["debug"]>=1:
        print(f"Debug 1 - FAILURE - Unable to enerated cue for \"{title}\"")
    return False

# calculates min sec and frames for cue files
def cue_time(time):
    if settings.config["debug"]>=2:
        print(f"Debug 2 - RUNNING - Entering CueTime")

    cueTime = {}
    cueTime["minutes"] = int(time // 60)
    cueTime["seconds"] = int(time % 60)
    cueTime["frames"]  = round(((time - math.floor(time)) * 75), 3) # one frame is 1/75 of a second

    return cueTime

# Generates the chapter information for the audiobookshelf metadata
def generate_cue_for_metadata(title: str, path: str) -> dict:
    if settings.config["debug"]>=1:
        print(f"Debug 1 - RUNNING - Generating chapter times for metadata")
    chapters = []

    bookFiles = enumerate_audiobook_folder(path)

    if len(bookFiles)>1:
        bookFiles.sort()

    for i, file in enumerate(bookFiles):
        fileName, fileExt = os.path.splitext(file)
        previousChapter = {}
        # for if the source is m4b
        if fileExt.lower()==".m4b":
            m4b = MP4(f"{path}/{file}")

            for n, chapter in enumerate(m4b.chapters):
                # used to identify the last chapter in a book
                if n==len(m4b.chapters)-1:
                    previousChapter["end"] = round(chapter.start, 3)
                    chapters.append(previousChapter)
                    finalChapter = {
                        "start": round(chapter.start, 3),
                        "end": round(m4b.info.length, 3),
                        "title": chapter.title,
                        "id": n
                    }
                    chapters.append(finalChapter)

                # Identify the first chapter in book
                elif n==0:
                    previousChapter = {
                        "start": 0,
                        "end": None,
                        "title": chapter.title,
                        "id": n
                    }

                # identify any other chapter
                else:
                    previousChapter["end"] = round(chapter.start, 3)
                    chapters.append(previousChapter)
                    previousChapter = {
                        "start": round(chapter.start, 3),
                        "end": None,
                        "title": chapter.title,
                        "id": n
                    }

        # for if the source is an mp3
        elif fileExt.lower()==".mp3":
            totalTime = 0

            mp3 = MP3(f"{path}/{file}")
            if i==len(bookFilesMP3)+1:
                previousChapter["end"] = round(totalTime, 3)
                chapters.append(previousChapter)
                finalChapter = {
                    "start": round(totalTime, 3),
                    "end": round((totalTime + float(mp3.info.length)), 3),
                    "title": fileName,
                    "id": i
                }
                chapters.append(finalChapter)

            # Identify the first chapter in book
            elif i==0:
                previousChapter = {
                    "start": 0,
                    "end": mp3.info.length,
                    "title": fileName,
                    "id": i
                }

            # identify any other chapter
            else:
                previousChapter["end"] = round(totalTime, 3)
                chapters.append(previousChapter)
                previousChapter = {
                    "start": round(totalTime, 3),
                    "end": None,
                    "title": fileName,
                    "id": i
                }

            totalTime += float(mp3.info.length)
                    

    if settings.config["debug"]>=1:
        print(f"Debug 1 - SUCCESS - Generating chapter times for metadata") 
    return chapters
    
    return False

def enumerate_audiobook_folder(path: str) -> list:
    bookFiles = []
    for file in os.listdir(path):
        fileName, fileExt = os.path.splitext(file)
        if fileExt.lower()==".mp3" or fileExt.lower()==".m4b":
            bookFiles.append(file)
    return bookFiles