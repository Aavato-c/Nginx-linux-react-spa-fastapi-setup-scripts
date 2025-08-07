from typing import Optional
import subprocess
import paramiko

from consts import (
    APP_CONFIGS_FOLDER, 
    DESTINATION_DIR_IP_FOR_CONFIGS, 
    SSH_COMMAND_PREFIX, 
    SSH_KEY_PATH, 
    SUPERVISOR_SERVER_PROCESS_NAME, 
    VPS_IP, 
    VPS_USER_NAME)



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

    # Upload the file to the VPS
    try:
        args = [
            "rsync", 
            "-av", 
        ] + exclude_patterns + [
            "\""+APP_CONFIGS_FOLDER+"\"", 
            DESTINATION_DIR_IP_FOR_CONFIGS
            ]
        if " " in APP_CONFIGS_FOLDER:
            # Handle spaces in the path
            args[3] = f"'{APP_CONFIGS_FOLDER}'"
        res = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = res.stdout
        stderr = res.stderr
        if res.returncode != 0:
            print(f"Rsync failed with exit code {res.returncode}. Output: {stdout.decode()}\nError: {stderr.decode()}")
            raise Exception(f"Rsync failed with exit code {res.returncode}. Output: {stdout.decode()}\nError: {stderr.decode()}")
        print("Rsync command executed successfully.")
        print(f"Rsync output: {stdout.decode()}")
        print(f"Rsync output: {res}")
        if res == 0:
            print("Configuration files have been synchronized to the server successfully.")
        else:
            print(f"Error while synchronizing configuration files to the server. Exit code: {res}")
        
    except Exception as e:
        print(f"Error while uploading folder to VPS: {e}")
        raise e

def reload_configs_on_vps(pass_for_user: Optional[str] = None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    commands_to_run = [
        f"{SSH_COMMAND_PREFIX}supervisorctl stop {SUPERVISOR_SERVER_PROCESS_NAME}",
        f"{SSH_COMMAND_PREFIX}supervisorctl reload",
        f"{SSH_COMMAND_PREFIX}supervisorctl start {SUPERVISOR_SERVER_PROCESS_NAME}",
        f"{SSH_COMMAND_PREFIX}systemctl restart nginx",
    ]
    
    key = paramiko.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
    ssh.connect(VPS_IP, port=22, username=VPS_USER_NAME, pkey=key)
    try:
        result_string = ""
        for command in commands_to_run:
            stdin, stdout, stderr = ssh.exec_command(command)
            result_string += f"\n\nCommand: {command.replace(SSH_COMMAND_PREFIX, '')}\nStdout: {stdout.read().decode()}\nStderr: {stderr.read().decode()}"
    finally:
        result_string = result_string if result_string else "No commands run"
        ssh.close()
    print(result_string)
    return result_string

def stop_program():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()
    key = paramiko.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
    ssh.connect(VPS_IP, port=22, username=VPS_USER_NAME, pkey=key)
    try:
        commands_to_run = [
            f"{SSH_COMMAND_PREFIX}supervisorctl stop {SUPERVISOR_SERVER_PROCESS_NAME}",
        ]
        result_string = ""
        for command in commands_to_run:
            stdin, stdout, stderr = ssh.exec_command(command)
            result_string += f"\n\nCommand: {command.replace(SSH_COMMAND_PREFIX, '')}\nStdout: {stdout.read().decode()}\nStderr: {stderr.read().decode()}"
    finally:
        try:
            result_string = result_string if result_string else "No commands run"
        except Exception as e:
            result_string = f"Error while processing result: {e}"
                                  
        ssh.close()
    print(result_string)
    return result_string

