import os, json, sys, shutil

# exit libro-tea
def exit_libro_tea():
    debug_mes(0, "END", "Exiting Libro-Tea")
    sys.exit()

# sets global enviorment configs
def get_config() -> dict:
    global version
    global config

    version = "beta"
    # Declare intial global config
    config = {
        "catalog_only":    get_env_var("LIBRO_TEA_catalog_only", False),
        "export_cover":    get_env_var("LIBRO_TEA_export_cover", True),
        "export_metadata": get_env_var("LIBRO_TEA_export_metadata", True),
        "export_cue":      get_env_var("LIBRO_TEA_export_cue", True),
        "force_download":  get_env_var("LIBRO_TEA_force_download", False),
        "rename_to_title": get_env_var("LIBRO_TEA_rename_to_title", True),
        "clear_working":   get_env_var("LIBRO_TEA_clear_working", True),
        "prefered_output": get_env_var("LIBRO_TEA_prefered_output", "M4B"),
        "account_file":    get_env_var("LIBRO_TEA_account_file", "account.json"),
        "account_dir":     get_env_var("LIBRO_TEA_account_dir", "./"),
        "config_file":     get_env_var("LIBRO_TEA_config_file", "config.json"),
        "config_dir":      get_env_var("LIBRO_TEA_config_dir", "./"),
        "database_file":   get_env_var("LIBRO_TEA_database_file", "library.db"),
        "database_dir":    get_env_var("LIBRO_TEA_database_dir", "./"),
        "output_dir":      get_env_var("LIBRO_TEA_output_dir", "./Audiobooks"),
        "working_dir":     get_env_var("LIBRO_TEA_working_dir", "/tmp/librotea"),
        "debug":           get_env_var("LIBRO_TEA_debug", 0)
    }

    # sets env/default config in the event a incomplete config file is used
    configDefault = config

    # setting config to expected values for command line args
    if sys.argv[1:]:
        config["catalog_only"]    = False
        config["export_cover"]    = False
        config["export_metadata"] = False
        config["export_cue"]      = False
        config["forced_download"] = False
        config["rename_to_title"] = False
        return config

    # Loads config from file if found
    if (os.path.exists(f"{config["config_dir"]}{config["config_file"]}")):
        with open(f"{config["config_dir"]}{config["config_file"]}", "r") as file:
            config = json.loads(file.read())

        # Checks for all fields from user config file and adds those not found from default.
        for key in configDefault:
            if config.get(key) == None:
                config[key] = configDefault[key]

            # makes the debug value a int if not already
            if key=="debug":
                config["debug"] = int(config["debug"])

        return config

    return config

# Overrides any config value if an enviroment variable is found
def env_var_over_ride(configPar, currentValue):
    for key in os.environ.keys():
        envVar = "LIBRO_TEA_" + configPar
        if key.lower() == envVar.lower():
            foundEnvVar = os.environ.get(key)

            if foundEnvVar.lower()=="false":
                return False
            elif foundEnvVar.lower()=="true":
                return True
            else:
                return foundEnvVar 

    return currentValue

# gets case insenstive env variables, This is an old bit of code in the event it is need
def get_env_var(envVar, defaultValue):
    for key in os.environ.keys():
        if key.lower() == envVar.lower():
            foundEnvVar = os.environ.get(key)

            # makes the debug value a int if not already
            if envVar.lower()=="libro_tea_debug":
                return int(foundEnvVar)

            if foundEnvVar.lower()=="false":
                return False
            elif foundEnvVar.lower()=="true":
                return True
            else:
                return foundEnvVar

    return defaultValue

# gets docker Secret values; no debug in here, it is a secret after all
def get_docker_secret_value(secret_file) -> str:
    if os.environ.get(secret_file).startswith("/run/secrets/"):
        with open(secret_file, "r") as secret:
            secret_value = file.read(secret)
        return secret_value

    normal_value = os.environ.get(secret_file)
    return normal_value

# Displays system and debug messages. done without logger.
# settings.debug_mes(, "", f"")
def debug_mes(debug_lvl: int, mes_status:str, mes: str) -> None:
    if config["debug"] >= debug_lvl:
        match debug_lvl:
            case _ if debug_lvl == 1:
                print(f"DEBUG 1 - {mes_status.capitalize().center(7)} - {mes}")
                return
            case _ if debug_lvl >= 2:
                print(f"DEBUG 2 - {mes_status.capitalize().center(7)} - {mes}")
                return
            case _:
                print(f"SYS MES - {mes_status.capitalize().center(7)} - {mes}")
                return
    else:
        return

# Lists book files in a folder
def enumerate_audiobook_folder(path: str) -> list:
    bookFiles = []

    for file in os.listdir(path):
        fileName, fileExt = os.path.splitext(file)
        if fileExt.lower()==".mp3" or fileExt.lower()==".m4b":
            bookFiles.append(file)

    return bookFiles
    
# Moves books out of the working folder
def move_from_working(title: str, workingPath: str, finalPath: str) -> bool:
    debug_mes(0, "Running", f"Moving audiobook files for \"{title}\" out of working folder.")

    bookFiles = enumerate_audiobook_folder(workingPath)

    try:
        for file in bookFiles:
            fileName, fileExt = os.path.splitext(file) 
            shutil.move(f"{workingPath}/{fileName}{fileExt}",f"{finalPath}/{fileName}{fileExt}")
            debug_mes(1, "Success", f"Finished moving audiobook files for \"{title}\"")
        
        return True

    except:
        debug_mes(0, "Failure", f"Unable to move audiobook files for \"{title}\"")
        return False

# Clears temp files
def clear_working_files(folder) -> None:
    debug_mes(1, "RUNNING", f"Cleaning up working folder")
    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            path = os.path.join(root, file)
            os.remove(path)
            debug_mes(2, "delete", f"file {path}")

        for directory in dirs:
            path = os.path.join(root, directory)
            os.rmdir(path)
            debug_mes(2, "delete", f"dir {path}")

    return

