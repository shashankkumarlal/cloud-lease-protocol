import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LEASE_FILE = BASE_DIR / "leases.json"

print("CLP STORE FILE PATH:", LEASE_FILE.resolve())


def load_leases():
    if not LEASE_FILE.exists():
        return {}

    try:
        with open(LEASE_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except json.JSONDecodeError:
        return {}


def save_all_leases(data: dict):
    with open(LEASE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_lease(lease):
    data = load_leases()
    data[lease.lease_id] = lease.to_dict()
    save_all_leases(data)

def update_lease(lease_id, updated_data):
    data = load_leases()
    if lease_id not in data:
        raise Exception("Lease not found")

    data[lease_id].update(updated_data)
    save_all_leases(data)
