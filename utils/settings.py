import os, json, sys

# exit libro-tea
def exit_libro_tea():
    sys.exit("SYS MES -   END   - Exiting Libro-Tea")

# sets global enviorment configs
def get_config() -> dict:
    global version
    global config

    version = "1.0"
    # Declare intial global config
    config = {
        "catalog_only":    get_env_var("LIBRO-TEA_catalog_only", False),
        "export_cover":    get_env_var("LIBRO-TEA_export_cover", True),
        "export_metadata": get_env_var("LIBRO-TEA_export_metadata", True),
        "export_cue":      get_env_var("LIBRO-TEA_export_cue", True),
        "force_download":  get_env_var("LIBRO-TEA_force_download", False),
        "rename_to_title": get_env_var("LIBRO-TEA_rename_to_title", True),
        "prefered_output": get_env_var("LIBRO-TEA_prefered_output", "M4B"),
        "account_file":    get_env_var("LIBRO-TEA_account_file", "account.json"),
        "account_dir":     get_env_var("LIBRO-TEA_account_dir", "./"),
        "config_file":     get_env_var("LIBRO-TEA_config_file", "config.json"),
        "config_dir":      get_env_var("LIBRO-TEA_config_dir", "./"),
        "database_file":   get_env_var("LIBRO-TEA_database_file", "library.db"),
        "database_dir":    get_env_var("LIBRO-TEA_database_dir", "./"),
        "output_dir":      get_env_var("LIBRO-TEA_output_dir", "./Audiobooks"),
        "working_dir":     get_env_var("LIBRO-TEA_working_dir", "./"),
        "debug":           get_env_var("LIBRO-TEA_debug", 0)
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

# gets case insenstive env variables
def get_env_var(envVar, defaultValue):
    for key in os.environ.keys():
        if key.lower()==envVar.lower():
            foundEnvVar = os.environ.get(key)

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

#if __name__ == "__main__":