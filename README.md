# Cloud Lease Protocol (CLP)

**Cloud Lease Protocol (CLP)** is a lease-based control-plane system that enforces
time-bound cloud infrastructure lifecycle using explicit, irreversible contracts.

Instead of relying on humans to remember cleanup, CLP guarantees that
temporary infrastructure **cannot outlive its intended lifetime**.

---

## 🚨 The Problem

In real-world cloud environments:

- Developers spin up EC2 instances “temporarily”
- CI/CD pipelines crash before cleanup steps run
- Hackathon or demo infrastructure is forgotten
- Incident-response servers remain exposed
- Cloud bills grow silently over time
- Security risk increases due to orphaned resources

The root cause is not tooling — it is **human unreliability**.

Most cloud platforms implicitly assume:

> “Someone will remember to clean this up.”

**CLP removes that assumption entirely.**

---

## 🧠 Core Idea

> **Infrastructure is not owned indefinitely — it is borrowed for a fixed time.**

Every managed cloud resource must have:

1. A **lease**
2. A **hard expiry time**
3. A **death contract** defining what happens at expiry

When the lease expires, CLP **enforces lifecycle automatically**.

No prompts.  
No dashboards.  
No heuristics.  

Only deterministic enforcement.

---

## 📦 What Is a Lease?

A **lease** is an explicit contract that defines how long a resource is allowed to exist.

Each lease contains:

- **Resource ID** (e.g., EC2 instance ID)
- **Issued timestamp**
- **Expiry timestamp**
- **State** (`ACTIVE` → `EXPIRED`)
- **Death contract**

### Example Lease

```text
Resource: i-0abc123
Issued at: 2026-01-19 06:27 UTC
Expires at: 2026-01-19 06:37 UTC
State: ACTIVE
Death contract: SNAPSHOT_TERMINATE
```

A lease is the single source of truth for lifecycle decisions.

## ☠️ Death Contracts
- CLP supports explicit post-expiry actions called death contracts.

Supported contracts:
TERMINATE
Immediately destroy the resource.

SNAPSHOT_TERMINATE
Create snapshots of attached storage, then destroy the resource.

ARCHIVE
Preserve data before removal (extensible).
Death behavior is explicit, deterministic, and irreversible.

## Complete Lifecycle (End-to-End)

1️⃣ Lease Issuance
A human or system creates infrastructure and explicitly specifies how long it may exist.
```ttl_minutes = 120```
CLP computes
```expires_at = issued_at + ttl```

2️⃣ Resource Binding
The resource is tagged to bind it to the lease:
```CLP_MANAGED = true```
```CLP_LEASE_ID = <lease-id>```

3️⃣ Time Passes

CLP does nothing.
No monitoring
No CPU checks
No traffic analysis
No heuristics
Time alone determines lifecycle.

4️⃣ Enforcement

When CLP runs, it evaluates a single condition:
```now ≥ expires_at```
If true:

Lease state transitions to EXPIRED
Death contract is enforced
Action is irreversible

5️⃣ Lease Renewal (Optional)
Before expiry, a user may explicitly renew a lease:
```python -m clp_agent.agent renew <LEASE_ID>```

Rules:

Renewal is allowed only while the lease is ACTIVE
Expired leases are immutable
Enforcement is guaranteed if renewal does not occur
Renewal is a conscious signal that the resource is still needed.

## 🔐 Safety Guarantees

CLP enforces multiple hard safety invariants:
Only explicitly tagged resources are managed
Lease-to-resource binding is validated
Expired leases cannot be renewed
Dry-run mode prevents accidental destruction
Deterministic behavior across restarts
No reliance on metrics or heuristics

## ☁️ AWS Integration
CLP integrates with AWS using boto3 and least-privilege IAM permissions.
Validated AWS actions:
Describe EC2 instances
Create EBS snapshots
Terminate EC2 instances
Termination and snapshot enforcement were tested end-to-end on real AWS EC2 instances.

## 🧪 Verified Behavior

Lease persistence across restarts
Deterministic expiry enforcement
Snapshot + termination on expiry
Dry-run safety mode
Real AWS execution

## 🎯 Real-World Use Cases

Dev & test environment cleanup
CI/CD ephemeral infrastructure
Hackathons and training environments
Incident-response and forensics servers
Security hardening
Cloud cost governance
Internal platform guardrails

## 🚀 Future Extensions

Grace periods and expiry warnings
Slack / email notifications
REST API for lease management
Lambda / EventBridge automation
Multi-resource leases
Kubernetes integration
