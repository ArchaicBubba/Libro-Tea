import sys
if __name__ == "__main__":
    from utils import account, cmdArg, settings, libraryManagement, downloader
else:
    from .utils import account, cmdArg, settings, libraryManagement, downloader


def start_libro_tea() -> bool:
    try:
        settings.get_config()

        parsedAccount = {}
        parsedArg = {}

        if sys.argv[1:]:
            parsedArg = cmdArg.sys_arg_controller(sys.argv[1:])
            if not parsedArg.get("email")==None and not parsedArg.get("password")==None:
                parsedAccount = {"email": parsedArg["email"], "password": parsedArg["password"]}

        settings.debug_mes(0, "start", "Starting Libro-Tea")

        libraryManagement.create_library()

        accounts = account.set_accounts(parsedAccount)

        if len(accounts) == 0:
            settings.debug_mes(0, "Error", "No Libro.fm accounts Detected")
            if __name__ == "__main__":
                cmdArg.sys_arg_help() # EXIT
            return False

        # loads all books into library
        downloader.catalog(accounts)

        if settings.config["catalog_only"]:
            return True

        if "isbn" in parsedArg:
            downloader.download_by_isbn(accounts, parsedArg["isbn"])
            if settings.config["clear_working"]:
                settings.clear_working_files(settings.config["working_dir"])
            return True

        if settings.config["force_download"]:
            downloader.force_download_all(accounts)
            if settings.config["clear_working"]:
                settings.clear_working_files(settings.config["working_dir"])
            return True

        settings.debug_mes(0, "Running", "Checking for new Audiobooks")

        downloader.download_only_new(accounts)
        
        if settings.config["clear_working"]:
            settings.clear_working_files(settings.config["working_dir"])
            return True
        return True
        
    except Exception as e:
        settings.debug_mes(0, "ERROR", f"Libro-Tea encountered an error. Error: {e}. Exiting Libro-Tea")
        return False

if __name__ == "__main__":
    start_libro_tea()

    settings.exit_libro_tea() # EXIT
