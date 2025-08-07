import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("tools_and_utils")[0]
sys.path.append(ROOT_DIR)

from tools_and_utils.consts import (API_ENTRY_POINT, 
                    GUNICORN_PROCESS_NAME, 
                    GUNICORN_PROCESS_WORKERS, 
                    GUNICORN_START_SCRIPT_PATH, 
                    LOG_LEVEL, 
                    NAME_OF_NGINX_UPSTREAM, 
                    NGINX_API_CONFIG_SAVE_PATH, 
                    NGINX_SPA_CONFIG_SAVE_PATH, 
                    SERVER_DOMAIN_TLD_API, 
                    SERVER_DOMAIN_TLD_SPA, 
                    SUPERVISOR_CONFIG_SAVE_PATH, 
                    SUPERVISOR_SERVER_PROCESS_NAME, 
                    UNIX_SOCKET_PATH, 
                    UVICORN_WORKER_CLASS, 
                    VPS_LOCATION_OF_API, 
                    VPS_LOCATION_OF_SPA, 
                    VPS_LOG_DIR, 
                    VPS_USER_NAME)


def write_nginx_config_for_react_router(
    log_dir: str = VPS_LOG_DIR,
    save_path: str = NGINX_SPA_CONFIG_SAVE_PATH,
    server_domain_tld: str = SERVER_DOMAIN_TLD_SPA,
    dir_of_spa: str = VPS_LOCATION_OF_SPA  # e.g., "/usr/share/nginx/frontend-app" or "/var/www/html"
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
        nginx_upstream_name: str = NAME_OF_NGINX_UPSTREAM, 
        nginx_socket_path: str = UNIX_SOCKET_PATH,
        server_domain_tld: str = SERVER_DOMAIN_TLD_API,
        log_dir_name: str = VPS_LOG_DIR,
        save_path: str = NGINX_API_CONFIG_SAVE_PATH
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
        supervisor_process_name: str = SUPERVISOR_SERVER_PROCESS_NAME,
        gunicorn_start_script_path: str = GUNICORN_START_SCRIPT_PATH,
        save_path: str = SUPERVISOR_CONFIG_SAVE_PATH,
        log_dir: str = VPS_LOG_DIR,
        log_file_name: str = "supervisor.log",
        user_name_for_process: str = VPS_USER_NAME,
        ):
    supervisor_config = f"""\
[program:{supervisor_process_name}]
    command={gunicorn_start_script_path}
    user={user_name_for_process}
    autostart=true
    autorestart=true
    redirect_stderr=true
    stdout_logfile={log_dir}/{log_file_name}
    stdout_logfile_maxbytes=50MB
    stdout_logfile_backups=10
    stderr_logfile={log_dir}/error_{log_file_name}
    stderr_logfile_maxbytes=50MB
    stderr_logfile_backups=10
"""
    if not os.path.exists(os.path.dirname(save_path)):
        input(f"Directory {os.path.dirname(save_path)} does not exist. Will we create it? Press Enter to continue or Ctrl+C to exit.")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        f.write(supervisor_config)

def write_gunicorn_start_script(
        directory_of_app: str = VPS_LOCATION_OF_API,
        log_dir: str = VPS_LOG_DIR,
        log_file_name: str = f"{GUNICORN_PROCESS_NAME}.log",
        nginx_socket_path: str = UNIX_SOCKET_PATH,
        user_name: str = VPS_USER_NAME,
        name_of_server_program: str = GUNICORN_PROCESS_NAME,
        num_of_workers: int = GUNICORN_PROCESS_WORKERS,
        save_path_for_script: str = GUNICORN_START_SCRIPT_PATH,
        uvicorn_worker_class: str = UVICORN_WORKER_CLASS,
        log_level: str = LOG_LEVEL,
        main_entry_point: str = API_ENTRY_POINT,  # e.g., "app.main:app"
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

if __name__ == "__main__":
    write_nginx_config()
    write_supervisor_config()
    write_gunicorn_start_script()
    write_nginx_config_for_react_router()
    print("Configuration files have been written successfully.")
    