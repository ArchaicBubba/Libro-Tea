import settings
import json, os

# Gets accounts from an account.json file OR from environment variables
def set_accounts():
    if settings.config["debug"]>=1:
        print("DEBUG 1 - RUNNING - Finding Libro.FM accounts.")
    if (os.path.exists("account.json")):
        if settings.config["debug"]>=1:
            print("DEBUG 1 - SUCCESS - Account.json file found; setting accounts from JSON.")
        with open("account.json", "r") as file:
            accounts = json.loads(file.read())
            if settings.config["debug"]==2:
                print(f"DEBUG 2 - RUNNING - Loaded {len(accounts)} accounts from file.")
            envAccounts = set_accounts_from_env_var(len(accounts))
            jsonAccountNum = len(accounts)
            # Adds any environment accounts that were not inclued in the json. Libro-Tea reads accounts as if they in a json format regardless of where they came from.
            for i, account in enumerate(envAccounts):
                newAccountNum = i + jsonAccountNum
                accounts[f"{newAccountNum}"] = envAccounts[account]
            return accounts
    accounts = set_accounts_from_env_var(0)
    return accounts

# Gets account infromation from the environment variables; breaks out Secrets when found
def set_accounts_from_env_var(numAccounts):
    if settings.config["debug"]>=1:
        print("DEBUG 1 - RUNNING - Looking for Libro.FM accounts in environment")
    user = []
    password = []
    i = 0
    accounts = {}
    for key in os.environ.keys():
        if key.startswith("account_user_"):
            user.append(key)
        if key.startswith("account_password_"):
            password.append(key)
    user.sort()
    password.sort()
    for i in range(len(user)):
        account = {
            "email": settings.get_docker_secret_value(user[i]),
            "password": settings.get_docker_secret_value(password[i])
        }
        accounts[f"{numAccounts}"] = account
        i += 1
        numAccounts += 1
    return accounts
