import os, json

# sets global enviorment configs
def get_config():
    print("SYS MES - RUNNING - Setting global settings")
    global config
    config = {
        "catalog_only":    os.environ.get("catalog_only", False), # overrides all, Does not download; Will make folder and catalogs audiobooks in database
        "export_cover":    os.environ.get("export_cover", True),
        "export_metadata": os.environ.get("export_metadata", True),
        "export_cue":      os.environ.get("export_cue", True),
        "force_download":  os.environ.get("force_download", False),
        "prefered_output": os.environ.get("prefered_output", "M4B"), # M4B or MP3
        "output_dir":      os.environ.get("output_dir", "./Audiobooks"),
        "working_dir":     os.environ.get("working_dir", "./"),
        "debug":           os.environ.get("debug", 0) # 1 for normal debug; 2 for obsesive
    }
    if (os.path.exists("config.json")):
        with open("config.json", "r") as file:
            config = json.loads(file.read())
            try:
                if config["debug"]>=1:
                    print(f"DEBUG 1 - RUNNING - Settings found in config.json; this will override any enviorment config!")
            except:
                config["debug"] = 1
                if config["debug"]>=1:
                    print(f"DEBUG 1 -  ERROR  - Settings found in config.json; this will override any enviorment config! These settings are malformed! No Debug Settings found, Setting to 1")
        if config["debug"]>=1:
            print(f"DEBUG 1 - RUNNING - Settings imported. Checking for all values.")
        if "catalog_only" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No catalog_only setting found in config. Setting to default value!")
            config["catalog_only"] = os.environ.get("catalog_only", False)
        if "export_cover" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No export_cover setting found in config. Setting to enviorment / default value!")
            config["export_cover"] = os.environ.get("export_cover", True)
        if "export_metadata" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No export_metadata setting found in config. Setting to enviorment /  value!")
            config["export_metadata"] = os.environ.get("export_metadata", True)
        if "export_cue" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No export_cue setting found in config. Setting to enviorment /  value!")
            config["export_cue"] = os.environ.get("export_cue", False)
        if "force_download" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No force_download setting found in config. Setting to enviorment /  value!")
            config["force_download"] = os.environ.get("force_download", False)
        if "prefered_output" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No prefered_output setting found in config. Setting to enviorment /  value!")
            config["prefered_output"] = os.environ.get("prefered_output", "M4B")
        if "output_dir" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No output_dir setting found in config. Setting to enviorment /  value!")
            config["output_dir"] = os.environ.get("output_dir", "./Audiobooks")
        if "working_dir" not in config.keys():
            if config["debug"]>=1:
                print("DEBUG 1 - ERROR - No working_dir setting found in config. Setting to enviorment /  value!")
            config["working_dir"] = os.environ.get("working_dir", "./")

        return config

    return config

# gets docker Secret values; no debug in here, it is a secret after all
def get_docker_secret_value(secret_file):
    if os.environ.get(secret_file).startswith("/run/secrets/"):
        with open(secret_file, "r") as secret:
            secret_value = file.read(secret)
        return secret_value
    normal_value = os.environ.get(secret_file)
    return normal_value

if __name__ == "__main__":
    get_config()
