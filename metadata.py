import account, libraryManagment, settings
from librofm.client import LibroFMClient
from librofm.util import clean_filename
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
import os, json, requests, datetime

# Downloads the cover from LibroFM. Saves in audiobook folder.
def export_cover(audiobook, path):
    if not os.path.exists(path):
        print(f"SYS MES -  ERROR  - Unable to export cover for {audiobook.title}; File path \"{path}\" does not exist!")
        return
    fullURL = "https:" + audiobook.cover_url
    if settings.config["debug"]>=1:
        print(f"DEBUG 1 - SUCCESS - Starting cover download for {audiobook.title}, file path will be \"{path}/cover.jpg.\"")
    response = requests.get(fullURL)
    if response.status_code == 200:
        with open(f"{path}/cover.jpg", "wb") as f:
            f.write(response.content)
        if settings.config["debug"]>=2:
            print(f"DEBUG 2 - SUCCESS - Cover for {audiobook.title} downloaded!")
    else:
        print(f"SYS MES -  ERROR  - Unable to find {audiobook.title}'s cover")
    return

# creates a metadata Json for audiobookshelf. Saves in audiobook folder
def export_metadata(audiobook, path):
    # Stops if it cant find the specified book
    if not os.path.exists(path):
        if system.config["debug"]>=1:
            print(f"Debug 1 - ERROR - Unable to export metadata for {audiobook.title}; file path \"{path}\" does not exist!")
        return
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
    chapters = generate_cue_for_metadata(audiobook, path)
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
    return metadata

# Changes mp3/m4b files names to their book names
def rename_to_title(title, path):
    bookFilesM4B = []
    bookFilesMP3 = []
    for file in os.listdir(path):
        if file[-4:].lower()==".m4b":
            bookFilesM4B.append(file)
        if file[-4:].lower()==".mp3":
            bookFilesMP3.append(file)
    if bookFilesM4B:
        if len(bookFilesM4B)>1:
            bookFilesM4B.sort()
            n = 1
            for bookM4B in bookFilesM4B:
                if settings.config["debug"]>=1:
                    print(f"DEBUG 1 - RUNNING - Renaming \"{bookM4B}\" to \"{title} - part {n:03d}.m4b\"")
                os.rename(f"{path}/{bookM4B}", f"{path}/{title} - part {n:03d}.m4b")
                n += 1
        elif len(bookFilesM4B)==1: 
            if settings.config["debug"]>=1:
                print(f"DEBUG 1 - RUNNING - Renaming \"{bookFilesM4B[0]}\" to \"{title}.m4b\"")
            os.rename(f"{path}/{bookFilesM4B[0]}", f"{path}/{title}.m4b")
            return
    if bookFilesMP3:
        if len(bookFilesMP3)>1:
            bookFilesMP3.sort()
            n = 1
            for bookMP3 in bookFilesMP3:
                if settings.config["debug"]>=1:
                    print(f"DEBUG 1 - RUNNING - Renaming \"{bookMP3}\" to \"{title} - track {n:03d}.mp3\"")
                os.rename(f"{path}/{bookMP3}", f"{path}/{title} - track {n:03d}.mp3")
                n += 1
        elif len(bookFilesMP3)==1:
            if settings.config["debug"]>=1:
                print(f"DEBUG 1 - RUNNING - Renaming \"{bookFilesMP3[0]}\" to \"{title}.mp3\"")
            os.rename(f"{path}/{bookFilesMP3[0]}", f"{path}/{title}.mp3")
    return

# Identifies which source to genorate a cue file for
def export_cue(audiobook, path):
    for file in os.listdir(path):
        if file[-4:].lower()==".m4b":
            return export_cue_from_m4b(audiobook, path)
        elif file[-4:].lower()==".mp3":
            return generate_cue_from_mp3(audiobook, path)
    return False

# exports the cue file from an m4b's metadata
def export_cue_from_m4b(audiobook, path):
    m4b = MP4(f"{path}/{audiobook.title}.m4b")
    with open(f"{path}/{audiobook.title}.cue", "w") as f:
        i = 1
        f.write("REM Source: LibroFM genorated with Libro-Tea\nREM Extracted from M4B File\n")
        f.write(f"TITLE \"{audiobook.title}\"\n")
        f.write(f"FILE \"{audiobook.title}.m4b\"\n")
        for chapter in m4b.chapters:
            time = str(datetime.timedelta(seconds=chapter.start))
            f.write(f"\tTRACK {i} AUDIO\n\t\tTITLE \"{chapter.title}\"\n\t\tINDEX 01 {time[:-3]}\n")
            i += 1
    return True

# generates the cue file from the mp3s track length
def generate_cue_from_mp3(audiobook, path):
    bookFilesMP3 = []
    for file in os.listdir(path):
        if file[-4:].lower()==".mp3":
            bookFilesMP3.append(file)
    bookFilesMP3.sort()
    with open(f"{path}/{audiobook.title}.cue", "w") as f:
        i = 1
        totalTime = 0
        f.write("REM Source: LibroFM genorated with Libro-Tea\nREM Made from MP3 File length\n")
        f.write(f"TITLE \"{audiobook.title}\"\n")
        for file in bookFilesMP3:
            mp3 = MP3(f"{path}/{file}")
            time = str(datetime.timedelta(seconds=totalTime))
            if i==1:
                f.write(f"\tTRACK {i} AUDIO\n\t\tTITLE \"{file[:-4]}\"\n\t\tINDEX 01 {time}\n")
            else:
                f.write(f"\tTRACK {i} AUDIO\n\t\tTITLE \"{file[:-4]}\"\n\t\tINDEX 01 {time[:-3]}\n")
            totalTime += float(mp3.info.length)
            i += 1
    return True

# Generates the chapter information for the audiobookshelf metadata
def generate_cue_for_metadata(audiobook, path):
    chapters = []
    for file in os.listdir(path):
        # for if the source is m4b
        if file[-4:].lower()==".m4b":
            m4b = MP4(f"{path}/{audiobook.title}.m4b")
            for i, chapter in enumerate(m4b.chapters):
                # used to identify the last chapter in a book
                if i==len(m4b.chapters)-1:
                    previousChapter["end"] = round(chapter.start, 3)
                    chapters.append(previousChapter)
                    finalChapter = {
                        "start": round(chapter.start, 3),
                        "end": round(m4b.info.length, 3),
                        "title": chapter.title,
                        "id": i
                    }
                    chapters.append(finalChapter)
                # Identify the first chapter in book
                elif i==0:
                    previousChapter = {
                        "start": 0,
                        "end": None,
                        "title": chapter.title,
                        "id": i
                    }
                # identify any other chapter
                else:
                    previousChapter["end"] = round(chapter.start, 3)
                    chapters.append(previousChapter)
                    previousChapter = {
                        "start": round(chapter.start, 3),
                        "end": None,
                        "title": chapter.title,
                        "id": i
                    }
            return chapters
        # for if the source is an mp3
        elif file[-4:].lower()==".mp3":
            bookFilesMP3 = []
            for file in os.listdir(path):
                if file[-4:].lower()==".mp3":
                    bookFilesMP3.append(file)
            bookFilesMP3.sort()
            totalTime = 0
            for i, file in enumerate(bookFilesMP3):
                mp3 = MP3(f"{path}/{file}")
                time = str(datetime.timedelta(seconds=totalTime))
                if i==len(bookFilesMP3)-1:
                    previousChapter["end"] = round(totalTime, 3)
                    chapters.append(previousChapter)
                    finalChapter = {
                        "start": round(totalTime, 3),
                        "end": round((totalTime + float(mp3.info.length)), 3),
                        "title": file[:-4],
                        "id": i
                    }
                    chapters.append(finalChapter)
                # Identify the first chapter in book
                elif i==0:
                    previousChapter = {
                        "start": 0,
                        "end": mp3.info.length,
                        "title": file[:-4],
                        "id": i
                    }
                # identify any other chapter
                else:
                    previousChapter["end"] = round(totalTime, 3)
                    chapters.append(previousChapter)
                    previousChapter = {
                        "start": round(totalTime, 3),
                        "end": None,
                        "title": file[:-4],
                        "id": i
                    }
                totalTime += float(mp3.info.length)
            return chapters
    return 
