import account, settings, libraryManagment, downloader

if __name__ == "__main__":
    print("SYS MES -  START  - Starting Libro-Tea")

    settings.get_config()
    libraryManagment.create_library()
    accounts = account.set_accounts()
    if settings.config["catalog_only"]:
        downloader.catalog(accounts)
    else:
        if settings.config["force_download"]:
            downloader.force_download_all(accounts)
        else:
            downloader.download_only_new(accounts)
    print("SYS MES -   END   - Exiting Libro-Tea")
