from . import settings
import os, sys

def sys_arg_controller():
    if sys.argv[1:]==0:
        return False
    else:
        parsedArg = sys_arg_parser(sys.argv[1:])
    return parsedArg

def sys_arg_parser(arguments: list):
    parsedArg = {}
    previousArg = False
    command = None
    for argument in arguments:
        if previousArg:
            command = argument
            arg = previousArg
            previousArg = False
        else:
            arg = argument
        match arg.lower():
            case "-h" | "--help":
                sys_arg_help()

            case "-d" | "--dry-run":
                settings.config["catalog_only"] = True
                continue

            case "--export-cover":
                settings.config["export_cover"] = True
                continue

            case "--export-metadata":
                settings.config["export_metadata"] = True
                continue

            case "--export-cue":
                settings.config["export_cue"] = True
                continue

            case "--download-all":
                settings.config["force_download"] = True
                continue

            case "--rename-to-title":
                settings.config["rename_to_title"] = True
                continue

            case "-v" | "--debug":
                settings.config["debug"] = 1 
                continue

            case a if a.startswith("--download-one"):
                if "=" in arg:
                    arg, isbn = arg.split("=")
                    parsedArg["isbn"] = isbn
                elif not command == None:
                    parsedArg["isbn"] = command
                    command = None
                else:
                    previousArg = arg
                continue

            case "--output-path":
                if "=" in arg:
                    path = arg.split("=")
                    settings.config["output_dir"] = file[1]
                elif not command == None:
                    settings.config["output_dir"] = command
                    command = None
                else:
                    previousArg = arg
                continue

            case "--prefered-output":
                if "=" in arg:
                    fileFormat = arg.split("=")
                    settings.config["output_dir"] = fileFormat[1]
                elif not command == None:
                    settings.config["output_dir"] = command
                    command = None
                else:
                    previousArg = arg
                continue

            case a if a.startswith(("-u", "--user")):
                if "=" in arg:
                    arg, user = argPath.split("=")
                    parsedArg["email"] = user
                elif not command == None:
                    parsedArg["email"] = command
                    command = None
                else:
                    previousArg = arg
                continue

            case a if a.startswith(("-p", "--pass")):
                if "=" in arg:
                    arg, password = argPath.split("=")
                    parsedArg["password"] = password
                elif not command == None:
                    parsedArg["password"] = command
                    command = None
                else:
                    previousArg = arg

            case a if a.startswith("--account"):
                if "=" in arg:
                    file = parse_file_path_from_arg(arg)
                    settings.config["account_dir"] = file[0]
                    settings.config["account_file"] = file[1]
                elif not command == None:
                    file = parse_file_path(command)
                    settings.config["account_dir"] = file[0]
                    settings.config["account_file"] = file[1]
                else:
                    previousArg = arg
                continue

            case a if a.startswith("--database"):
                if "=" in arg:
                    file = parse_file_path_from_arg(arg)
                    settings.config["database_dir"] = file[0]
                    settings.config["database_file"] = file[1]
                elif not command == None:
                    file = parse_file_path(command)
                    settings.config["database_dir"] = file[0]
                    settings.config["database_file"] = file[1]
                else:
                    previousArg = arg
                continue

            case _:
                print(f"SYS MES -  ERROR  - Invalid Peramiter: {arg}")
                sys_arg_help()
                
    return parsedArg

# Gets file paths and names and seperates for user arguments
def parses_file_path(path: str):
    # checks if the file exists
    if "/" in path:
        fileName = os.path.basename(path)
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path))
        filePath = f"{os.path.dirname(path)}/"
        return filePath, fileName
    else:
        filePath = "./"
        fileName = path
    return filePath, fileName

# Pre processing for parses_file_path.
def parse_file_path_from_arg(argPath:str):
    path = argPath.split("=")
    file = parses_file_path(path[1])
    return file

# Help text for arguments 
def sys_arg_help():
    sys.exit(f"""\
Libro-Tea allows you to download all audiobooks owned by one or more Libro.fm accounts and organize them into a clean, Audiobookshelf ready structure.
  Libro-Tea version: {settings.version}
  When running Libro-Tea with arguments all True/False values are False unless otherwise stated.
  Commands:
    -h | --help: displays this message. Yes this one.
    -d | --dry-run: will create the output directories of all audiobooks to be downloaded. 
    -u | --user: Email LibroFM account. MUST HAVE PASS ARG.
    -p | --pass: Password for LibroFM account. MUST HAVE USER ARG.
         --export-cover: Downloads cover art from Libro.fm and places it in the audiobook folder.
         --export-cue: Generates or exports a CUE file and places it in audiobook folder.
         --export-metadata: Downloads cover art from Libro.fm and places it in audiobook folder.
         --rename-to-title: Renames the downloaded audiobook audio files to the title of the book.
         --download-one: Downloads a single book by specified ISBN. Must be owned by a used account.
         --download-all: Downloads all audiobooks, regardless of download status
         --output-path: Changes the audiobook folder name and location.
            Default "./Audiobook".
         --prefered-output: Prefered output format MP3 or M4B. 
            Default: m4b
         --account: Json file used to store accounts for downloading audiobooks. File path to location.
            Example: ./documents/account.json
         --database: SQL database used to hold download statuses. File path to database location.
            Example: ./music/Audiobooks/library.db
    -v | --debug: Displays additonal debugging messages
    """)