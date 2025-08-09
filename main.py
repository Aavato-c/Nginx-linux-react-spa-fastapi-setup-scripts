
from tools_and_utils.remote_utils import rsync_configs_to_server
from tools_and_utils.config_generation_utils import generate_all_configs
from tools_and_utils.logging import LoggingUtil

log = LoggingUtil(name="config_generation")

if __name__ == "__main__":
    generate_all_configs()
    print("Configuration files have been written successfully.")
    rsync_configs_to_server()
    print("Repository has been synchronized to the server successfully.")
