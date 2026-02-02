from utils import account, cmdArg, settings, libraryManagment, downloader
import sys


if __name__ == "__main__":
    settings.get_config()

    parsedAccount = {}
    parsedArg = {}

    if sys.argv[1:]:
        parsedArg = cmdArg.sys_arg_controller()
        if not parsedArg.get("email")==None and not parsedArg.get("password")==None:
            parsedAccount = {"email": parsedArg["email"], "password": parsedArg["password"]}

    print("SYS MES -  START  - Starting Libro-Tea")

    libraryManagment.create_library()

    accounts = account.set_accounts(parsedAccount)
    
    if len(accounts) == 0:
        print("SYS MES -  ERROR  - No Libro.fm accounts detected.")
        settings.exit_libro_tea() # EXIT

    if parsedArg.get("isbn"):
            downloader.download_by_isbn(accounts, parsedArg["isbn"])
            settings.exit_libro_tea() # EXIT

    if settings.config["catalog_only"]:
        downloader.catalog(accounts)
        settings.exit_libro_tea() # EXIT

    if settings.config["force_download"]:
        downloader.force_download_all(accounts)
        settings.exit_libro_tea() # EXIT

    downloader.download_only_new(accounts)
    settings.exit_libro_tea() # EXIT
    
