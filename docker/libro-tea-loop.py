import time, os, shutil
from program import librotea

# Stripped down debug, keeps things consistent
def sys_mes(mes_status:str, mes: str) -> None:
    print(f"SYS MES - {mes_status.capitalize().center(7)} - {mes}")
    return

def get_int_env_var(envVar, defaultValue) -> int:
    for key in os.environ.keys():
        if key.lower() == envVar.lower():
            foundEnvVar = os.environ.get(key)
            return int(foundEnvVar)

    return int(defaultValue)

def user_file_check(fileName) -> bool:
    sys_mes('check', f'Checking for user file \'{fileName}\'')
    if not (os.path.exists(f'/librotea/config/{fileName}.json')):
        if not os.path.exists(f'/librotea/config/{fileName}.json.example'):
            try:
                shutil.copyfile(f'/librotea/example/{fileName}.json.example', f'/librotea/config/{fileName}.json.example')
                sys_mes('notice', f'\'{fileName}.json\' not found. Using enviorment settings if found. Copied example file to config folder.')

            except:
                sys_mes('notice', f'\'{fileName}.json\' not found. Using enviorment settings if found.')
                sys_mes('warning', 'Unable to write to Config folder. Potential errors may occure.')

            return False

        sys_mes('notice', f'\'{fileName}.json\' not found. Using enviorment settings if found.')
        return False
    sys_mes('notice', f'\'{fileName}\' config found.')
    return True

sys_mes('First', 'Starting intial checks')

user_file_check('config')

user_file_check('account')

sleepSec = get_int_env_var('LIBRO_TEA_second', 0)
sleepMin = get_int_env_var('LIBRO_TEA_min', 30)
sleepHour = get_int_env_var('LIBRO_TEA_hour', 0)
sleepDay = get_int_env_var('LIBRO_TEA_day', 0)

sleepTime = int(sleepSec + (sleepMin * 60) + (sleepHour * 3600) + (sleepDay * 86400))

sys_mes('Pre', 'Entering Libro-Tea Process')

#'''
# Main libro-tea loop
while True:
    try:
        if not librotea.start_libro_tea():
            sys_mes('Exit', f'Libro-Tea reported an error while running. Exiting loop.')
            break

        sys_mes('sleep', f'Libro-Tea ran without error, checking again in {sleepTime} seconds')
        time.sleep(sleepTime)

    # outputs any error identified
    except Exception as e:
        sys_mes('Fatel', f'Libro-Tea exited unexpectedly. Error: {e}')
        break
#'''