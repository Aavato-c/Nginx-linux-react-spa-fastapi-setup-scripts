import json
import os
import sys
from typing import Optional

from tools_and_utils.models import SyncConfig

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("tools_and_utils")[0]
sys.path.append(ROOT_DIR)


from tools_and_utils.helpers import is_envvar_truthy, pythify_str
if not os.path.exists(f"{ROOT_DIR}/filesync.env.json"):
    with open(f"{ROOT_DIR}/filesync.env.json", "w") as f:
        config_base = {"root_dir": ROOT_DIR}
        json.dump(config_base, f, indent=4, ensure_ascii=False)

with open(f"{ROOT_DIR}/filesync.env.json", "r") as f:
    json_config = json.load(f)
config = SyncConfig.model_validate(json_config)

def raise_or_get_config_var(var_name: str, default_value: Optional[str] = None) -> str:
    """
    Raises an error if the environment variable is not set, or returns its value.
    If a default value is provided, it will return that instead if the variable is not set.
    """
    if config and hasattr(config, var_name):
        value = getattr(config, var_name)
        if value is None and default_value is not None:
            return default_value
        elif value is None:
            raise EnvironmentError(f"Configuration variable '{var_name}' is not set.")
        return value
    else:
        raise EnvironmentError(f"Configuration variable '{var_name}' is not set in the SyncConfig model.")

VPS_USER_NEEDS_PASSWORD = is_envvar_truthy(raise_or_get_config_var("vps_user_needs_password"))
_pass = None
if VPS_USER_NEEDS_PASSWORD:
    _pass = input("Enter password for VPS user: ")
    SSH_COMMAND_PREFIX = f"echo '{_pass}' | sudo -S "
else:
    SSH_COMMAND_PREFIX = "sudo "




VPS_USER_NAME = pythify_str(raise_or_get_config_var("vps_user_name"))
SSH_KEY_PATH = raise_or_get_config_var("ssh_key_path")
LOG_LEVEL = raise_or_get_config_var("log_level", default_value="info")

SERVER_DOMAIN_TLD_API = raise_or_get_config_var("server_domain_tld_api")
SERVER_DOMAIN_TLD_SPA = raise_or_get_config_var("server_domain_tld_spa")
VPS_LOG_DIR = os.path.join(pythify_str(SERVER_DOMAIN_TLD_API), "logs")

APP_NAME = pythify_str(raise_or_get_config_var("app_name"))

APP_CONFIGS_FOLDER_BASENAME = f"{APP_NAME}-configs"
APP_CONFIGS_FOLDER_RELATIVE = os.path.join("generated_configs", APP_CONFIGS_FOLDER_BASENAME)
APP_CONFIGS_FOLDER = os.path.join(ROOT_DIR, APP_CONFIGS_FOLDER_RELATIVE)
if not os.path.exists(APP_CONFIGS_FOLDER):
    os.makedirs(APP_CONFIGS_FOLDER)
SH_SCRIPTS_ENV_FILE = os.path.join(APP_CONFIGS_FOLDER, ".env.bash.scripts")

SUPERVISOR_SERVER_PROCESS_NAME = f"{APP_NAME}-supervisor-process"
GUNICORN_PROCESS_NAME = f"{APP_NAME}-gunicorn-process"

GUNICORN_PROCESS_WORKERS = int(raise_or_get_config_var("gunicorn_process_workers"))
UVICORN_WORKER_CLASS = "uvicorn.workers.UvicornWorker"

SUPERVISOR_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "supervisor-config.conf")
NGINX_API_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "nginx-api-config.conf")
NGINX_SPA_CONFIG_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "nginx-spa-config.conf")
GUNICORN_START_SCRIPT_SAVE_PATH = os.path.join(APP_CONFIGS_FOLDER, "gunicorn-start.sh")

SPA_APP_NAME = f"{APP_NAME}-spa"

VPS_IP = raise_or_get_config_var("vps_ip")
VPS_PORT = int(raise_or_get_config_var("vps_port", default_value=22))
API_ENTRY_POINT = raise_or_get_config_var("api_entry_point")

# Without trailing slash
VPS_LOCATION_OF_API = raise_or_get_config_var("vps_location_of_api")
VPS_LOCATION_OF_SPA = raise_or_get_config_var("vps_location_of_spa")

NAME_OF_NGINX_UPSTREAM = f"{GUNICORN_PROCESS_NAME.replace('-', '_')}_upstream"
UNIX_SOCKET_PATH = f"/tmp/{NAME_OF_NGINX_UPSTREAM}.sock"

DESTINATION_DIR = raise_or_get_config_var("scripts_destination_root_dir_on_vps")
DESTINATION_DIR_IP = f"{VPS_USER_NAME}@{VPS_IP}:{DESTINATION_DIR}"
DESTINATION_DIR_APP_CONFIGS = os.path.join(DESTINATION_DIR, APP_CONFIGS_FOLDER_BASENAME)
DESTINATION_DIR_FINAL_CONFIG = os.path.join(DESTINATION_DIR, APP_CONFIGS_FOLDER_BASENAME)
DESTINATION_DIR_IP_FOR_FINAL_CONFIGS = f"{VPS_USER_NAME}@{VPS_IP}:{DESTINATION_DIR_FINAL_CONFIG}"

GUNICORN_START_SCRIPT_VPS_PATH = os.path.join(DESTINATION_DIR_APP_CONFIGS, "gunicorn-start.sh")



