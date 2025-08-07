
from tools_and_utils.remote_utils import rsync_configs_to_server
from tools_and_utils.config_generation_utils import write_gunicorn_start_script, write_nginx_config, write_nginx_config_for_react_router, write_supervisor_config


if __name__ == "__main__":
    write_nginx_config()
    write_supervisor_config()
    write_gunicorn_start_script()
    write_nginx_config_for_react_router()

    print("Configuration files have been written successfully.")
    rsync_configs_to_server()
    print("Repository has been synchronized to the server successfully.")
