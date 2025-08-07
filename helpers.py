import os
import re
import unicodedata


def raise_or_get_env_var(var_name: str, default_value: str = None) -> str:
    value = os.getenv(var_name)
    if not value or value == "":
        if default_value is not None:
            return default_value
        else:
            raise ValueError(f"{var_name} is not set in the environment variables.")
    if "<--" in value:
        if default_value is not None:
            return default_value
        else:
            raise ValueError(f"{var_name} is not set in the environment variables. Please set it to a valid value.")
    return value

def pythify_str(string: str) -> str:
    value = str(string)
    
    # Normalize unicode characters to ASCII
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    
    if "." in value:
        value = value.replace(".", "-")

    # Remove non-alphanumeric characters except for underscores and hyphens
    value = re.sub(r'[^\w\s-]', '', value.lower())

    # Replace spaces and multiple hyphens with a single hyphen
    value = re.sub(r'[-\s]+', '-', value).strip('-_')

    # Ensure string does not start with a numeric character
    if value and value[0].isdigit():
        value = 'd-' + value

    # Ensure string is not empty
    if not value:
        value = 'default-name'
    return value

def is_envvar_truthy(envvar: str) -> bool:
    """
    Check if the environment variable is set to a truthy value.
    """
    return str(envvar).lower() in ("true", "1", "yes", "on")