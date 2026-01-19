from datetime import datetime, timedelta, timezone
import uuid


class Lease:
    def __init__(self, resource_id, ttl_minutes, death_contract):
        self.lease_id = str(uuid.uuid4())
        self.resource_id = resource_id
        self.issued_at = datetime.now(timezone.utc)
        self.ttl = timedelta(minutes=ttl_minutes)  # initial TTL
        self.expires_at = self.issued_at + self.ttl
        self.state = "ACTIVE"
        self.death_contract = death_contract

    def is_expired(self):
        return datetime.now(timezone.utc) >= self.expires_at

    def refresh_state(self):
        if self.is_expired():
            self.state = "EXPIRED"

    def renew(self, additional_minutes):
        self.refresh_state()

        if self.state != "ACTIVE":
            raise Exception("Cannot renew an expired lease")

        self.expires_at += timedelta(minutes=additional_minutes)
        self.ttl += timedelta(minutes=additional_minutes)

    def to_dict(self):
        return {
            "lease_id": self.lease_id,
            "resource_id": self.resource_id,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "state": self.state,
            "death_contract": self.death_contract,
        }

    def __str__(self):
        return (
            f"Lease(id={self.lease_id}, "
            f"resource={self.resource_id}, "
            f"expires_at={self.expires_at}, "
            f"state={self.state}, "
            f"death_contract={self.death_contract})"
        )
