import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).split("tools_and_utils")[0]
sys.path.append(ROOT_DIR)

from tools_and_utils.config_model import SyncConfig

if not os.path.exists(f"{ROOT_DIR}/filesync.env.json"):
    with open(f"{ROOT_DIR}/filesync.env.json", "w") as f:
        config_base = {"root_dir": ROOT_DIR}
        json.dump(config_base, f, indent=4, ensure_ascii=False)

with open(f"{ROOT_DIR}/filesync.env.json", "r") as f:
    json_config = json.load(f)
config = SyncConfig.model_validate(json_config)

CONFIG = config



