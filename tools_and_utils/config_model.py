import os
from typing import Optional
from pydantic import BaseModel, Field

from tools_and_utils.helpers import is_envvar_truthy, pythify_str



class SyncConfig(BaseModel):
    def __init__(self, **data):
        self.deletable_properties = set()
        super().__init__(**data)
        _pass = None
        if self.vps_user_needs_password:
            _pass = input("Enter password for VPS user: ")
            self.ssh_command_prefix = f"echo '{_pass}' | sudo -S "
        else:
            self.ssh_command_prefix = "sudo "

    vps_ip: Optional[str] = Field(None, description="IP address of the VPS")
    vps_port: Optional[int] = Field(None, description="Port number for the VPS")
    vps_user_name: Optional[str] = Field(None, description="Username for the VPS")
    ssh_key_path: Optional[str] = Field(None, description="Path to the SSH key")
    vps_user_needs_password: Optional[int] = Field(None, description="Indicates if the VPS user needs a password")
    vps_location_of_api: Optional[str] = Field(None, description="Location of the API on the VPS")
    vps_location_of_spa: Optional[str] = Field(None, description="Location of the SPA on the VPS")
    destination_root_dir_on_vps: Optional[str] = Field(None, description="Root directory for scripts on the VPS")
    api_entry_point: Optional[str] = Field(None, description="Entry point for the API")
    
    app_name: Optional[str] = Field(default="my_app", description="Name of the application")
    @property
    def app_name_pythified(self) -> str:
        return pythify_str(self.app_name)

    @property
    def app_name_pythified_underscore(self) -> str:
        return self.app_name_pythified.replace("-", "_")
    
    
    server_domain_tld_api: Optional[str] = Field(None, description="Top-level domain for the API")
    server_domain_tld_spa: Optional[str] = Field(None, description="Top-level domain for the SPA")
    
    gunicorn_process_workers: Optional[int] = Field(default=4, description="Number of Gunicorn workers")
    uvicorn_worker_class: str = "uvicorn.workers.UvicornWorker"
    ssh_command_prefix: Optional[str] = None
    
    root_dir: Optional[str] = Field(None, description="Root directory of the sync utilities")
    log_level: Optional[str] = Field(default="info", description="Logging level for the application")

        
    def deletable_property(self, func):
        """
        Decorator to mark a property as deletable.
        """
        deltable = func.__name__
        self.deletable_properties.add(deltable)
        return func

    @property
    def path_server_log_dir(self) -> str:
        return os.path.join(pythify_str(self.server_domain_tld_api), "logs")
    
    @property
    def basename_app_configs_folder(self) -> str:
        return f"{self.app_name}-configs"

    @property
    def path_local_app_configs_relative(self) -> str:
        return os.path.join("generated-configs", self.basename_app_configs_folder)

    @property
    def path_local_app_config_folder(self) -> str:
        return os.path.join(self.root_dir, self.basename_app_configs_folder)
    
    @property
    def name_server_supervisor_process(self) -> str:
        return f"{self.app_name_pythified_underscore}_supervisor_process"
    
    @property
    def name_server_gunicorn_process(self) -> str:
        return f"{self.app_name_pythified_underscore}_gunicorn_process"


    @property
    def basename_supervisor_config(self) -> str:
        return f"{self.app_name_pythified_underscore}_supervisor_config.conf"

    @deletable_property
    @property
    def filepath_local_supervisor_config(self) -> str:
        return os.path.join(self.path_local_app_config_folder, self.basename_supervisor_config)
    
    

    @property
    def filepath_local_nginx_api_config(self) -> str:
        return os.path.join(self.path_local_app_config_folder, "nginx-api-config.conf")

    @property
    def filepath_local_nginx_spa_config(self) -> str:
        return os.path.join(self.path_local_app_config_folder, "nginx-spa-config.conf")

    @property
    def filepath_local_gunicorn_start_script(self) -> str:
        return os.path.join(self.path_local_app_config_folder, "gunicorn-start.sh")

    @property
    def name_of_nginx_upstream(self) -> str:
        return f"{self.name_server_gunicorn_process}_upstream"

    @deletable_property
    @property
    def unix_socket_path(self) -> str:
        return f"/tmp/{self.name_of_nginx_upstream}.sock"


    @property
    def destination_dir_ip(self) -> str:
        return f"{self.vps_user_name}@{self.vps_ip}:{self.destination_root_dir_on_vps}"

    @property
    def vps_dir_app_configs(self) -> str:
        return os.path.join(self.destination_root_dir_on_vps, self.basename_app_configs_folder)

    @property
    def destination_dir_ip_for_final_configs(self) -> str:
        return f"{self.vps_user_name}@{self.vps_ip}:{self.vps_dir_app_configs}"

    @property
    def filepath_server_gunicorn_start_script(self) -> str:
        return os.path.join(self.vps_dir_app_configs, "gunicorn-start.sh")

    @property
    def path_server_supervisor_config(self) -> str:
        return os.path.join(self.vps_dir_app_configs, self.basename_supervisor_config)

    
    @property
    def files_to_be_created(self) -> list[str]:
        return [
            self.path_local_app_config_folder,
        ]

    @deletable_property
    @property
    def filepath_server_supervisor_linked(self) -> str:
        return f"/etc/supervisor/conf.d/{self.app_name}-supervisor-config.conf"

    @property
    def filepath_local_server_init_script(self) -> str:
        return self.path_local_app_config_folder + "/server_init.sh"
    
    @property
    def filepath_local_server_startup_script(self) -> str:
        return self.path_local_app_config_folder + "/server_startup.sh"

