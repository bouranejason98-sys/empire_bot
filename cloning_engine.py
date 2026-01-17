from memory_engine import MemoryEngine
from datetime import datetime

memory = MemoryEngine()

def resolve_clone(user, region="Kenya", clone_id=None):
    # If clone_id provided, fetch from registry
    if clone_id:
        return {"id": clone_id, "region": region}
    # Otherwise, create a dynamic clone
    new_id = f"{region}_clone_{int(datetime.utcnow().timestamp())}"
    memory.conn.execute("INSERT OR IGNORE INTO clones (id, region, niche, created_at) VALUES (?, ?, ?, ?)",
                        (new_id, region, "general", datetime.utcnow().isoformat()))
    memory.conn.commit()
    return {"id": new_id, "region": region}
