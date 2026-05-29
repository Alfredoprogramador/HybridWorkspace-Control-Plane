package hwcp.device_compliance

# Device Compliance Policy
# Defines minimum requirements for device trust levels

import rego.v1

# Minimum requirements for TRUSTED status
trusted_requirements := {
    "disk_encrypted": true,
    "antivirus_enabled": true,
    "os_up_to_date": true,
    "firewall_enabled": true,
    "screen_lock_enabled": true,
}

# Minimum requirements for CONDITIONAL access
conditional_requirements := {
    "disk_encrypted": true,
    "firewall_enabled": true,
}

# Calculate compliance score (0-100)
compliance_score := score if {
    passed_checks := {
        "disk_encrypted" | input.device.disk_encrypted == true
    } | {
        "antivirus_enabled" | input.device.antivirus_enabled == true
    } | {
        "os_up_to_date" | input.device.os_up_to_date == true
    } | {
        "firewall_enabled" | input.device.firewall_enabled == true
    } | {
        "screen_lock_enabled" | input.device.screen_lock_enabled == true
    }
    score := count(passed_checks) * 20
}

# Determine trust level
is_trusted if {
    input.device.disk_encrypted == true
    input.device.antivirus_enabled == true
    input.device.os_up_to_date == true
    input.device.firewall_enabled == true
    input.device.screen_lock_enabled == true
}

is_conditional if {
    not is_trusted
    input.device.disk_encrypted == true
    input.device.firewall_enabled == true
}

trust_level := "trusted" if is_trusted

trust_level := "conditional" if {
    not is_trusted
    is_conditional
}

trust_level := "untrusted" if {
    not is_trusted
    not is_conditional
}

# Is the device compliant (score >= 80)?
is_compliant if {
    compliance_score >= 80
}
