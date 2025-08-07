import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("tools_and_utils")[0]
sys.path.append(ROOT_DIR)

from typing import Optional
import subprocess
import paramiko

from tools_and_utils.consts import CONFIG



def rsync_configs_to_server():
    exclude_patterns = [
        "--exclude", "*.pyc",
        "--exclude", "__pycache__",
        "--exclude", "database.db",
        "--exclude", "*.git",
        "--exclude", "venv",
        "--exclude", "dist",
        "--exclude", "*.log",
        "--exclude", ".env",
        "--exclude", ".env.scripts",
        "--exclude", "*.pem",
        "--exclude", "*.pub",
    ]

    # Ensure the destination directory exists on the VPS
    execute_cmd_on_vps(f"{CONFIG.ssh_command_prefix}mkdir -p {CONFIG.destination_dir_ip_for_final_configs}")
    execute_cmd_on_vps(f"{CONFIG.ssh_command_prefix}chown -R {CONFIG.vps_user_name}:{CONFIG.vps_user_name} {CONFIG.destination_dir_ip_for_final_configs}")

    # Upload the file to the VPS
    try:
        args = [
            "rsync", 
            "-av", 
        ] + exclude_patterns + [
            f"{CONFIG.path_local_app_config_folder}/", 
            f"{CONFIG.destination_dir_ip_for_final_configs}/"
            ]
        if " " in CONFIG.path_local_app_config_folder:
            # Handle spaces in the path
            args[3] = f"'{CONFIG.path_local_app_config_folder}'"
        res = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = res.stdout.decode()
        stderr = res.stderr.decode()
        if res.returncode != 0:
            print(f"Rsync failed with exit code {res.returncode}. Output: {stdout}\nError: {stderr}")
            raise Exception(f"Rsync failed with exit code {res.returncode}. Output: {stdout}\nError: {stderr}")
        print("Rsync command executed successfully.")
        print(f"Rsync output: {stdout}")
        print(f"Rsync output: {res}")
        if res == 0:
            print("Configuration files have been synchronized to the server successfully.")
        else:
            print(f"Error while synchronizing configuration files to the server. Exit code: {res}")
        
    except Exception as e:
        raise e

def execute_cmd_on_vps(cmd: str,
                                vps_user_name: str = CONFIG.vps_user_name,
                                vps_ip: str = CONFIG.vps_ip,
                                vps_port: int = CONFIG.vps_port,
                                ssh_key_path: str = CONFIG.ssh_key_path,
                                ) -> str:
    """
    Create directories on the VPS if they do not exist.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()

    try:
        key = paramiko.Ed25519Key.from_private_key_file(ssh_key_path)
    except Exception as e:
        if "encountered RSA key, expected OPENSSH key" in str(e):
            key = paramiko.RSAKey.from_private_key_file(ssh_key_path)
        else:
            raise e

    ssh.connect(vps_ip, port=vps_port, username=vps_user_name, pkey=key)

    try:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout_str = stdout.read().decode()
        stderr_str = stderr.read().decode()
        if stdout_str:
            print(f"Output: {stdout_str}")
        if stderr_str:
            print(f"Error: {stderr_str}")
            raise Exception(f"Command failed with error: {stderr_str}")
        if stdout_str == "" and stderr_str == "":
            print(f"Command executed successfully: {cmd}")
            return True
        if not stderr_str:
            print(f"Command executed successfully: {cmd}")
            return True
    finally:
        ssh.close()

def reload_configs_on_vps():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    commands_to_run = [
        f"{CONFIG.ssh_command_prefix}supervisorctl stop {CONFIG.name_server_supervisor_process}",
        f"{CONFIG.ssh_command_prefix}supervisorctl reload",
        f"{CONFIG.ssh_command_prefix}supervisorctl start {CONFIG.name_server_supervisor_process}",
        f"{CONFIG.ssh_command_prefix}systemctl restart nginx",
    ]
    
    key = paramiko.Ed25519Key.from_private_key_file(CONFIG.ssh_key_path)
    ssh.connect(CONFIG.vps_ip, port=CONFIG.vps_port, username=CONFIG.vps_user_name, pkey=key)
    try:
        result_string = ""
        for command in commands_to_run:
            stdin, stdout, stderr = ssh.exec_command(command)
            result_string += f"\n\nCommand: {command.replace(CONFIG.ssh_command_prefix, '')}\nStdout: {stdout.read().decode()}\nStderr: {stderr.read().decode()}"
    finally:
        result_string = result_string if result_string else "No commands run"
        ssh.close()
    print(result_string)
    return result_string

def stop_program():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    key = paramiko.Ed25519Key.from_private_key_file(CONFIG.ssh_key_path)
    ssh.connect(CONFIG.vps_ip, port=CONFIG.vps_port, username=CONFIG.vps_user_name, pkey=key)
    try:
        commands_to_run = [
            f"{CONFIG.ssh_command_prefix}supervisorctl stop {CONFIG.name_server_supervisor_process}",
        ]
        result_string = ""
        for command in commands_to_run:
            stdin, stdout, stderr = ssh.exec_command(command)
            result_string += f"\n\nCommand: {command.replace(CONFIG.ssh_command_prefix, '')}\nStdout: {stdout.read().decode()}\nStderr: {stderr.read().decode()}"
    finally:
        try:
            result_string = result_string if result_string else "No commands run"
        except Exception as e:
            result_string = f"Error while processing result: {e}"
                                  
        ssh.close()
    print(result_string)
    return result_string

