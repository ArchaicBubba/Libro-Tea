from . import settings, cmdArg
import json, os

# Gets accounts from an account.json file OR from environment variables
def set_accounts(parsedAccount):
    if settings.config["debug"]>=1:
        print("DEBUG 1 - RUNNING - Finding Libro.FM accounts.")

    accounts = {}

    if (os.path.exists(f"{settings.config["account_dir"]}/{settings.config["account_file"]}")):
        if settings.config["debug"]>=1:
            print("DEBUG 1 - SUCCESS - Account.json file found; setting accounts from JSON.")

        with open(f"{settings.config["account_dir"]}{settings.config["account_file"]}", "r") as file:
            accounts = json.loads(file.read())
        if settings.config["debug"]==2:
            print(f"DEBUG 2 - RUNNING - Loaded {len(accounts)} accounts from file.")

        # Adds any environment accounts that were not inclued in the json. Libro-Tea reads accounts as if they in a json format regardless of where they came from.
        envAccounts = set_accounts_from_env_var(len(accounts))

        for account in envAccounts:
            accounts[f"{len(accounts)}"] = envAccounts[account]

        if not parsedAccount.get("email")==None and not parsedAccount.get("password")==None:
            accounts[f"{len(accounts)}"] = parsedAccount

        return accounts

    accounts = set_accounts_from_env_var(0)

    if not parsedAccount.get("email")==None and not parsedAccount.get("password")==None:
        accounts[f"{len(accounts)}"] = parsedAccount

    return accounts


# Gets account infromation from the environment variables; breaks out Secrets when found
def set_accounts_from_env_var(numAccounts: int):
    if settings.config["debug"]>=1:
        print("DEBUG 1 - RUNNING - Looking for Libro.FM accounts in environment")

    user = []
    password = []
    accounts = {}

    for key in os.environ.keys():
        if key.startswith("Libro_FM_account_user_"):
            user.append(key)
        if key.startswith("Libro_FM_account_password_"):
            password.append(key)

    user.sort()
    password.sort()

    for i in range(len(user)):
        account = {
            "email": settings.get_docker_secret_value(user[i]),
            "password": settings.get_docker_secret_value(password[i])
        }
        accounts[f"{i}"] = account

    return accounts
