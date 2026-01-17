# cloning_engine.py

import json
import os
from datetime import datetime

class CloneManager:
    def __init__(self, base_config_path="clone_configs"):
        self.base_config_path = base_config_path
        os.makedirs(self.base_config_path, exist_ok=True)

    def create_clone(self, region, niche, currency="USD"):
        clone_id = f"{region.lower()}_{niche.lower()}_{int(datetime.utcnow().timestamp())}"
        clone_config = {
            "clone_id": clone_id,
            "region": region,
            "niche": niche,
            "currency": currency,
            "created_at": datetime.utcnow().isoformat(),
            "agents_enabled": True,
            "predictive_engine": True,
            "self_healing": True,
            "status": "active"
        }

        file_path = os.path.join(self.base_config_path, f"{clone_id}.json")
        with open(file_path, "w") as f:
            json.dump(clone_config, f, indent=4)

        return clone_config
