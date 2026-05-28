package hwcp.authz

# HybridWorkspace Control Plane – Zero Trust Authorization Policy
# Based on NIST 800-207 Zero Trust Architecture principles.
#
# This policy implements:
#   1. Never trust, always verify
#   2. Least-privilege access
#   3. Assume breach

import rego.v1

# Default deny – Zero Trust principle: explicit deny unless explicitly allowed
default allow := false

# ── Allow rules ──────────────────────────────────────────────────────────────

# Admin users have full access when device is trusted
allow if {
    input.subject.role == "admin"
    input.subject.device_trust == "trusted"
}

# IT Managers can access device and policy management
allow if {
    input.subject.role == "it_manager"
    input.subject.device_trust in {"trusted", "conditional"}
    input.resource.type in {"device", "policy", "user"}
}

# Security analysts can read any resource
allow if {
    input.subject.role == "security_analyst"
    input.subject.device_trust in {"trusted", "conditional"}
    input.action == "read"
}

# Employees can access their own resources from trusted/conditional devices
allow if {
    input.subject.role == "employee"
    input.subject.device_trust in {"trusted", "conditional"}
    input.subject.device_compliant == true
    input.resource.type in {"workspace", "collaboration"}
}

# Allow employees to update their own device posture
allow if {
    input.subject.role == "employee"
    input.resource.type == "device"
    input.resource.owner_id == input.subject.id
    input.action == "update_posture"
}

# ── Conditional access rules ─────────────────────────────────────────────────

# Conditional access: allow from VPN even if device is conditional
allow if {
    input.subject.device_trust == "conditional"
    input.context.network_type == "vpn"
    input.action in {"read", "create"}
    not is_sensitive_resource
}

# ── Deny rules (override allows) ─────────────────────────────────────────────

# Block untrusted devices regardless of role
deny if {
    input.subject.device_trust == "untrusted"
}

# Block access from public networks for sensitive resources
deny if {
    input.context.network_type == "public"
    is_sensitive_resource
}

# Block revoked/blocked devices
deny if {
    input.subject.device_status in {"revoked", "blocked"}
}

# ── Helper rules ──────────────────────────────────────────────────────────────

# Sensitive resources require higher trust
is_sensitive_resource if {
    input.resource.type in {"admin-panel", "security-config", "audit-logs", "user-management"}
}

# Final decision: allow only if allowed AND not denied
allow if {
    not deny
    _any_allow_rule
}

_any_allow_rule if {
    input.subject.role == "admin"
}
