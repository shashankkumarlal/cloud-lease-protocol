from datetime import datetime, timezone, timedelta
from .lease import Lease
from .store import load_leases, save_lease, save_all_leases
from .enforcer import enforce_death_contract
from .death_contracts import DeathContract
import sys

print("CLP Agent starting...")

# =========================
# MODE 1 — RENEW LEASE
# =========================
if len(sys.argv) == 3 and sys.argv[1] == "renew":
    lease_id = sys.argv[2]
    leases = load_leases()

    lease = leases.get(lease_id)
    if not lease:
        print("Lease not found")
        sys.exit(1)

    expires_at = datetime.fromisoformat(lease["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        print("Cannot renew expired lease")
        sys.exit(1)

    expires_at += timedelta(minutes=10)
    lease["expires_at"] = expires_at.isoformat()

    save_all_leases(leases)
    print(f"Lease {lease_id} renewed by 10 minutes")
    sys.exit(0)

# =========================
# MODE 2 — ENFORCE EXPIRIES
# =========================
print("Checking existing leases for expiry...")

all_leases = load_leases()
now = datetime.now(timezone.utc)

changed = False

for lease_id, data in all_leases.items():
    expires_at = datetime.fromisoformat(data["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now >= expires_at and data["state"] == "ACTIVE":
        data["state"] = "EXPIRED"
        changed = True
        print(f"Lease {lease_id} expired.")

        enforce_death_contract(
            resource_id=data["resource_id"],
            death_contract=data.get(
                "death_contract",
                DeathContract.TERMINATE
            )
        )

if changed:
    save_all_leases(all_leases)

# =========================
# MODE 3 — CREATE NEW LEASE
# =========================
lease = Lease(
    resource_id="i-0aca2f665a6c27b11",
    ttl_minutes=1,
    death_contract=DeathContract.SNAPSHOT_TERMINATE
)

print("Lease created:")
print(lease)

save_lease(lease)
print("Lease saved to disk.")
