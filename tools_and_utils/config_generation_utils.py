import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("tools_and_utils")[0]
sys.path.append(ROOT_DIR)

from tools_and_utils.consts import CONFIG

def write_nginx_config_for_react_router(
    log_dir: str = CONFIG.path_server_log_dir,
    save_path: str = CONFIG.filepath_local_nginx_spa_config,
    server_domain_tld: str = CONFIG.server_domain_tld_api,
    dir_of_spa: str = CONFIG.vps_location_of_spa  # e.g., "/usr/share/nginx/frontend-app" or "/var/www/html"
    ):
    
    nginx_config= f"""\
server {{
    listen 80;
    error_log {log_dir}/nginx-spa-error.log;
    access_log {log_dir}/nginx-spa-access.log;
    server_name {server_domain_tld};
    location / {{
            root {dir_of_spa};
            try_files $uri /index.html;
    }}
}}"""
    if not os.path.exists(os.path.dirname(save_path)):
        input(f"Directory {os.path.dirname(save_path)} does not exist. Will we create it? Press Enter to continue or Ctrl+C to exit.")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        f.write(nginx_config)
    return nginx_config



def write_nginx_config(
        nginx_upstream_name: str = CONFIG.name_of_nginx_upstream, 
        nginx_socket_path: str = CONFIG.unix_socket_path,
        server_domain_tld: str = CONFIG.server_domain_tld_api,
        log_dir_name: str = CONFIG.path_server_log_dir,
        save_path: str = CONFIG.filepath_local_nginx_api_config
        ):
    nginx_config = f"""\
upstream {nginx_upstream_name} {{
        server unix:{nginx_socket_path} fail_timeout=0;
}}

server {{
        client_max_body_size 4G;
        access_log {log_dir_name}/nginx-access.log;
        
        error_log {log_dir_name}/nginx-error.log;
        server_name {server_domain_tld};
        keepalive_timeout 5;

        location / {{
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_redirect off;

                if (!-f $request_filename) {{
                        proxy_pass http://{nginx_upstream_name};
                        break;
                }}
        }}

}}
server {{
    listen 80;
    listen [::]:80;
    server_name {server_domain_tld};
    # server_name <domain>.<tld> www.<domain>.<tld>;
}}
    """

    if not os.path.exists(os.path.dirname(save_path)):
        input(f"Directory {os.path.dirname(save_path)} does not exist. Will we create it? Press Enter to continue or Ctrl+C to exit.")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        f.write(nginx_config)

def write_supervisor_config(
        supervisor_process_name: str = CONFIG.name_server_supervisor_process,
        gunicorn_start_script_path: str = CONFIG.filepath_server_gunicorn_start_script,
        save_path: str = CONFIG.filepath_local_supervisor_config,
        log_dir: str = CONFIG.path_server_log_dir,
        user_name_for_process: str = CONFIG.vps_user_name,
        ):
    supervisor_config = f"""\
[program:{supervisor_process_name}]
    command={gunicorn_start_script_path}
    user={user_name_for_process}
    autostart=true
    autorestart=true
    redirect_stderr=true
    
    stdout_logfile={log_dir}/{supervisor_process_name}.log
    stdout_logfile_maxbytes=50MB
    stdout_logfile_backups=10
    
    stderr_logfile={log_dir}/{supervisor_process_name}_error.log
    stderr_logfile_maxbytes=50MB
    stderr_logfile_backups=10
"""
    with open(save_path, "w") as f:
        f.write(supervisor_config)

def write_gunicorn_start_script(
        directory_of_app: str = CONFIG.vps_location_of_api,
        log_dir: str = CONFIG.path_server_log_dir,
        log_file_name: str = f"{CONFIG.name_server_gunicorn_process}.log",
        nginx_socket_path: str = CONFIG.unix_socket_path,
        user_name: str = CONFIG.vps_user_name,
        name_of_server_program: str = CONFIG.name_server_gunicorn_process,
        num_of_workers: int = CONFIG.gunicorn_process_workers,
        save_path_for_script: str = CONFIG.filepath_local_gunicorn_start_script,
        uvicorn_worker_class: str = CONFIG.uvicorn_worker_class,
        log_level: str = CONFIG.log_level,
        main_entry_point: str = CONFIG.api_entry_point,  # e.g., "app.main:app"
        ):

    gunicorn_start_script = f"""#!/bin/sh
cd {directory_of_app}
# source venv/bin/activate (If you have problems, use this instead of the one below)
. venv/bin/activate
exec gunicorn "{main_entry_point}" \\
--name {name_of_server_program} \\
--workers {num_of_workers} \\
--worker-class {uvicorn_worker_class} \\
--user {user_name} \\
--group {user_name} \\
--bind {nginx_socket_path} \\
--log-level {log_level} \\
--log-file {log_dir}/{log_file_name} \\
"""
    if not os.path.exists(os.path.dirname(save_path_for_script)):
        input(f"Directory {os.path.dirname(save_path_for_script)} does not exist. Will we create it? Press Enter to continue or Ctrl+C to exit.")
    os.makedirs(os.path.dirname(save_path_for_script), exist_ok=True)
    with open(save_path_for_script, "w") as f:
        f.write(gunicorn_start_script)

def chmod_to_executable(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    try: 
        os.chmod(file_path, 0o755)  # Make the file executable
        return True
    except Exception as e:
        print(f"Error making file {file_path} executable: {e}")
        raise e

def create_server_init_script(
        save_path: str = CONFIG.filepath_local_server_init_script
    ):
    init_script = f"""\
#!/bin/bash

sudo apt update && sudo apt upgrade -y

# Install basic utils
sudo apt install -y curl git nginx


# Install supervisor if not installed
if ! command -v supervisorctl &> /dev/null
then
    echo "Installing supervisor"
    sudo apt install supervisor
else
    #TODO
fi


# Install homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Adding it to path
    test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
    test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc
"""
    with open(save_path, "w") as f:
        f.write(init_script)

def create_server_app_initiation_script(
        save_path: os.PathLike = CONFIG.filepath_local_server_startup_script
    ):
    startup_script = f"""\
#!bin/bash

curr_dir=$(pwd)
this_file_path=$(realpath "$0")
cd "$(dirname "$this_file_path")" || exit 1

CONFIG_FOLDER="{CONFIG.path_local_app_config_folder}"
NAME_OF_SERVER_PROGRAM="{CONFIG.name_server_gunicorn_process}"
SUPERVISOR_CONFIG_PATH="{CONFIG.path_server_supervisor_config}"
basename_supervisor_config="{CONFIG.basename_supervisor_config}"
GUNICORN_START_SCRIPT_PATH="{CONFIG.filepath_server_gunicorn_start_script}"

sudo chmod +x $GUNICORN_START_SCRIPT_PATH
sudo ln -s $SUPERVISOR_CONFIG_PATH {CONFIG.filepath_server_supervisor_linked}

# Start supervisor
sudo service supervisor start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start $NAME_OF_SERVER_PROGRAM
sudo supervisorctl status $NAME_OF_SERVER_PROGRAM    
"""
    with open(save_path, "w") as f:
        f.write(startup_script)


def generate_all_configs():
    write_nginx_config_for_react_router()
    write_nginx_config()
    write_supervisor_config()
    write_gunicorn_start_script()
    create_server_init_script()
    create_server_app_initiation_script()
    chmod_to_executable(CONFIG.filepath_local_gunicorn_start_script)
    chmod_to_executable(CONFIG.filepath_local_server_init_script)
    chmod_to_executable(CONFIG.filepath_local_server_startup_script)
        
if __name__ == "__main__":
    generate_all_configs()
    print("Configuration files have been written successfully.")
    