from typing import Optional
from pydantic import BaseModel, Field



class SyncConfig(BaseModel):
    vps_ip: Optional[str] = Field(None, description="IP address of the VPS")
    vps_port: Optional[int] = Field(None, description="Port number for the VPS")
    vps_user_name: Optional[str] = Field(None, description="Username for the VPS")
    ssh_key_path: Optional[str] = Field(None, description="Path to the SSH key")
    vps_user_needs_password: Optional[int] = Field(None, description="Indicates if the VPS user needs a password")
    vps_location_of_api: Optional[str] = Field(None, description="Location of the API on the VPS")
    vps_location_of_spa: Optional[str] = Field(None, description="Location of the SPA on the VPS")
    scripts_destination_root_dir_on_vps: Optional[str] = Field(None, description="Root directory for scripts on the VPS")
    api_entry_point: Optional[str] = Field(None, description="Entry point for the API")
    app_name: Optional[str] = Field(default="my_app", description="Name of the application")
    server_domain_tld_api: Optional[str] = Field(None, description="Top-level domain for the API")
    server_domain_tld_spa: Optional[str] = Field(None, description="Top-level domain for the SPA")
    gunicorn_process_workers: Optional[int] = Field(default=4, description="Number of Gunicorn workers")
    
    root_dir: Optional[str] = Field(None, description="Root directory of the sync utilities")
    log_level: Optional[str] = Field(default="info", description="Logging level for the application")