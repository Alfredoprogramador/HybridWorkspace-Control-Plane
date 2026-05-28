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
    checks := [
        1 | input.device.disk_encrypted == true,
        1 | input.device.antivirus_enabled == true,
        1 | input.device.os_up_to_date == true,
        1 | input.device.firewall_enabled == true,
        1 | input.device.screen_lock_enabled == true,
    ]
    score := count([c | c := checks[_]; c == 1]) * 20
}

# Determine trust level
trust_level := "trusted" if {
    input.device.disk_encrypted == true
    input.device.antivirus_enabled == true
    input.device.os_up_to_date == true
    input.device.firewall_enabled == true
    input.device.screen_lock_enabled == true
}

trust_level := "conditional" if {
    not trust_level == "trusted"
    input.device.disk_encrypted == true
    input.device.firewall_enabled == true
}

trust_level := "untrusted" if {
    not trust_level == "trusted"
    not trust_level == "conditional"
}

# Is the device compliant (score >= 80)?
is_compliant if {
    compliance_score >= 80
}
