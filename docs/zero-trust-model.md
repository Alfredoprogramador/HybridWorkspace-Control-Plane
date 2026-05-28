# Zero Trust Architecture Model

## Overview

The HybridWorkspace Control Plane implements **Zero Trust Architecture (ZTA)** based on the principles defined in [NIST SP 800-207](https://doi.org/10.6028/NIST.SP.800-207) and the **BeyondCorp** model developed by Google.

**Core Principle**: Never trust, always verify. Every access request — regardless of network location — must be authenticated, authorized, and continuously validated.

---

## Seven Tenets of Zero Trust (NIST 800-207)

1. **All data sources and computing services are resources**  
   Every device, user, and service is a potential resource and must be managed accordingly.

2. **All communication is secured regardless of network location**  
   Network location (internal vs. external) grants no implicit trust. All communication uses mTLS/TLS.

3. **Access to individual enterprise resources is granted on a per-session basis**  
   Access is granted session-by-session, not permanently. Tokens expire and are continuously re-validated.

4. **Access to resources is determined by dynamic policy**  
   Policies consider user identity, device health, behavioral context, and environmental factors.

5. **The enterprise monitors and measures the integrity and security posture of all owned assets**  
   Device agents continuously report posture. Non-compliant devices lose access automatically.

6. **All resource authentication and authorization is dynamic and strictly enforced**  
   The Policy Engine (OPA) evaluates every request. No bypass mechanisms exist.

7. **The enterprise collects as much information as possible to improve security posture**  
   All events are logged and analyzed. Behavioral analytics detect anomalies.

---

## Architecture Components

### Control Plane

The central nervous system of the platform:

```
┌─────────────────────────────────────────────────────────────┐
│                    Control Plane                             │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Policy      │  │  Identity    │  │  Device          │  │
│  │  Engine      │  │  Provider    │  │  Registry        │  │
│  │  (OPA)       │  │  (SSO)       │  │  (MDM)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Audit Log   │  │  Threat      │  │  VPN Orchestr.   │  │
│  │  Service     │  │  Detection   │  │  (Headscale)     │  │
│  │              │  │  (AI)        │  │                  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Trust Engine

The Trust Engine calculates a **continuous trust score** for every device:

| Score | Trust Level | Access Granted |
|-------|-------------|----------------|
| ≥ 90  | **TRUSTED** | Full access to all authorized resources |
| 60-89 | **CONDITIONAL** | Limited access; sensitive resources blocked |
| < 60  | **UNTRUSTED** | No access granted (VPN blocked) |
| N/A   | **BLOCKED** | Explicitly denied; under investigation |

#### Compliance Factors (weighted)

| Factor | Weight | Description |
|--------|--------|-------------|
| Disk Encryption | 25% | Full disk encryption (BitLocker, FileVault, LUKS) |
| Antivirus | 20% | Active, up-to-date AV solution |
| OS Up-to-Date | 20% | Latest security patches installed |
| Firewall | 20% | Host-based firewall enabled |
| Screen Lock | 15% | Automatic screen lock configured |

### Policy Evaluation Flow

```
Request → Identity Verification → Device Posture Check → Context Analysis
    ↓
Policy Engine (OPA)
    ↓
Decision: ALLOW / DENY / CONDITIONAL
    ↓
Audit Log → Response
```

### VPN Architecture (Zero Trust Network Access)

We use **Tailscale** (with self-hosted **Headscale** control server) implementing **WireGuard** for:
- Mutual authentication between all nodes
- End-to-end encrypted tunnels
- Split-tunnel routing based on policies
- Continuous re-authentication via device certificates

---

## Continuous Verification

Unlike traditional perimeter-based security, the platform continuously verifies:

1. **Identity**: JWT tokens expire every 30 minutes; device tokens expire every 24 hours
2. **Device Posture**: Agent reports posture every 15 minutes
3. **Context**: Network type, location, and time-of-day are factored into every decision
4. **Behavior**: AI models detect anomalies in user/device behavior

---

## Policy as Code

All access policies are defined in **Rego** (OPA's policy language) and stored in `packages/ai-policies/rego/`. This enables:
- Version control for all policy changes
- Automated policy testing in CI/CD
- Rapid policy deployment without service restart
- Policy simulation and impact analysis

### Example Policy (Rego)

```rego
package hwcp.authz

# Default deny
default allow := false

# Allow trusted employees to access workspace resources
allow if {
    input.subject.role == "employee"
    input.subject.device_trust == "trusted"
    input.subject.device_compliant == true
    input.resource.type == "workspace"
}
```

---

## Compliance Mappings

| Framework | Relevant Controls | Status |
|-----------|------------------|--------|
| NIST 800-207 | All ZTA tenets | ✅ Implemented |
| ISO 27001 | A.9 (Access Control), A.12 (Operations) | 🔄 In Progress |
| SOC 2 | CC6.1-CC6.8 (Logical Access) | 🔄 In Progress |
| LGPD | Art. 46-49 (Security measures) | 🔄 In Progress |

---

## Threat Model

### Assets Protected
- Corporate data and intellectual property
- Internal systems and services
- User credentials and identity data
- Device fleet and configurations

### Threat Actors
- External attackers attempting unauthorized access
- Compromised credentials (phishing, credential stuffing)
- Insider threats (malicious or negligent employees)
- Compromised devices (malware, physical theft)

### Mitigations
- MFA for all users (TOTP + hardware keys supported)
- Device certificates with short lifetimes
- Behavioral analytics for anomaly detection
- Network segmentation via VPN policies
- Least-privilege access by default
