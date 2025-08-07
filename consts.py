

import os

import dotenv

from helpers import is_envvar_truthy, pythify_str, raise_or_get_env_var


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(f"{ROOT_DIR}/.env.scripts"):
    raise FileNotFoundError(f".env.scripts file not found in {ROOT_DIR}. Please create it with the required environment variables.")

dotenv.load_dotenv(f"{ROOT_DIR}/.env.scripts")
dotenv.set_key(dotenv.find_dotenv(f"{ROOT_DIR}/.env.scripts"), "ROOT_DIR", ROOT_DIR)

VPS_USER_NEEDS_PASSWORD = is_envvar_truthy(raise_or_get_env_var("VPS_USER_NEEDS_PASSWORD"))
_pass = None
if VPS_USER_NEEDS_PASSWORD:
    _pass = input("Enter password for VPS user: ")
    SSH_COMMAND_PREFIX = f"echo '{_pass}' | sudo -S "
else:
    SSH_COMMAND_PREFIX = "sudo "





VPS_USER_NAME = pythify_str(raise_or_get_env_var("VPS_USER_NAME"))
SSH_KEY_PATH = raise_or_get_env_var("SSH_KEY_PATH")
LOG_LEVEL = raise_or_get_env_var("LOG_LEVEL", default_value="info")

SERVER_DOMAIN_TLD_API = raise_or_get_env_var("SERVER_DOMAIN_TLD_API")
SERVER_DOMAIN_TLD_SPA = raise_or_get_env_var("SERVER_DOMAIN_TLD_SPA")
VPS_LOG_DIR = os.path.join(pythify_str(SERVER_DOMAIN_TLD_API), "logs")

APP_NAME = pythify_str(raise_or_get_env_var("APP_NAME"))

APP_CONFIGS_FOLDER_BASENAME = f"{APP_NAME}-configs"
APP_CONFIGS_FOLDER_RELATIVE = os.path.join("generated_configs", APP_CONFIGS_FOLDER_BASENAME)
APP_CONFIGS_FOLDER = os.path.join(ROOT_DIR, APP_CONFIGS_FOLDER_RELATIVE)
if not os.path.exists(APP_CONFIGS_FOLDER):
    os.makedirs(APP_CONFIGS_FOLDER)
SH_SCRIPTS_ENV_FILE = os.path.join(APP_CONFIGS_FOLDER, ".env.bash.scripts")

SUPERVISOR_SERVER_PROCESS_NAME = f"{APP_NAME}-supervisor-process"
GUNICORN_PROCESS_NAME = f"{APP_NAME}-gunicorn-process"

GUNICORN_PROCESS_WORKERS = int(raise_or_get_env_var("GUNICORN_PROCESS_WORKERS"))
UVICORN_WORKER_CLASS = "uvicorn.workers.UvicornWorker"

SUPERVISOR_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "supervisor-config.conf")
GUNICORN_START_SCRIPT_PATH = os.path.join(APP_CONFIGS_FOLDER, "gunicorn-start.sh")
NGINX_API_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "nginx-api-config.conf")
NGINX_SPA_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "nginx-spa-config.conf")

SPA_APP_NAME = f"{APP_NAME}-spa"

VPS_IP = raise_or_get_env_var("VPS_IP")
VPS_PORT = int(raise_or_get_env_var("VPS_PORT", default_value=22))
API_ENTRY_POINT = raise_or_get_env_var("API_ENTRY_POINT")

# Without trailing slash
VPS_LOCATION_OF_API = raise_or_get_env_var("VPS_LOCATION_OF_API")
VPS_LOCATION_OF_SPA = raise_or_get_env_var("VPS_LOCATION_OF_SPA")

NAME_OF_NGINX_UPSTREAM = f"{GUNICORN_PROCESS_NAME}-upstream"
UNIX_SOCKET_PATH = f"/tmp/{NAME_OF_NGINX_UPSTREAM}.sock"

DESTINATION_DIR = raise_or_get_env_var("SCRIPTS_DESTINATION_ROOT_DIR_ON_VPS")
DESTINATION_DIR_IP = f"{VPS_USER_NAME}@{VPS_IP}:{DESTINATION_DIR}"
DESTINATION_DIR_APP_CONFIGS = os.path.join(DESTINATION_DIR, APP_CONFIGS_FOLDER_BASENAME)
DESTINATION_DIR_FINAL_CONFIG = os.path.join(DESTINATION_DIR, APP_CONFIGS_FOLDER_BASENAME)
DESTINATION_DIR_IP_FOR_FINAL_CONFIGS = f"{VPS_USER_NAME}@{VPS_IP}:{DESTINATION_DIR_FINAL_CONFIG}"


bash_scripts_env_template = f"""\
VPS_IP={VPS_IP}
VPS_USER_NAME={VPS_USER_NAME}
"""

bash_scripts_save_path = os.path.join(APP_CONFIGS_FOLDER, ".env.bash.scripts")
if not os.path.exists(os.path.dirname(bash_scripts_save_path)):
    os.makedirs(os.path.dirname(bash_scripts_save_path), exist_ok=True)
    with open(bash_scripts_save_path, "w") as f:
        f.write(bash_scripts_env_template)