# Privacy Policy – HybridWorkspace Control Plane

**Effective Date**: January 2025  
**Last Updated**: January 2025

---

## 1. Overview

The HybridWorkspace Control Plane is an enterprise security platform designed to protect organizational resources while respecting the privacy of employees. This document outlines what data is collected, how it is used, and the rights employees have regarding their information.

Our platform is designed on **Privacy by Design** principles:
- Data minimization: we collect only what is strictly necessary for security purposes
- Purpose limitation: data is used only for the purposes described in this policy
- Employee transparency: all monitoring is disclosed and consented to

---

## 2. Data We Collect

### 2.1 Device Security Data

**What we collect:**
- Device hardware information (model, serial number, OS version)
- Security posture indicators (encryption status, antivirus status, firewall status, OS patch level, screen lock configuration)
- Network connectivity data (IP address, VPN status)
- Device agent version and health status

**What we do NOT collect:**
- Personal files, documents, or photos
- Browsing history on personal browsers
- Personal application usage
- Keystrokes or screen content
- Personal emails or messages

### 2.2 Authentication & Access Data

**What we collect:**
- Login timestamps and authentication events
- Failed authentication attempts
- Access logs for corporate resources (which resource, when, from which device)
- MFA setup and verification events

**What we do NOT collect:**
- Passwords (only cryptographic hashes are stored)
- Personal account credentials for non-corporate services

### 2.3 Behavioral Analytics (Opt-in / Disclosed)

When behavioral analytics are enabled by the organization:
- Access patterns to corporate resources
- Anomalous activity flags (for security investigation only)
- Session duration and frequency for corporate applications

**Important**: Behavioral analytics are aggregated and anonymized. Individual employee productivity is not monitored or reported without legal basis.

---

## 3. Legal Basis for Processing

We process personal data under the following legal bases:

| Data Category | Legal Basis | Justification |
|--------------|-------------|---------------|
| Device posture | Legitimate interest | Required for Zero Trust security |
| Authentication logs | Legal obligation | Regulatory compliance (ISO 27001, SOC 2) |
| Access logs | Legitimate interest | Security incident investigation |
| Behavioral analytics | Consent | Explicit employee notification required |

---

## 4. Data Retention

| Data Type | Retention Period | Justification |
|-----------|-----------------|---------------|
| Device posture history | 90 days | Compliance investigation window |
| Authentication logs | 1 year | Security audit requirements |
| Access logs | 1 year | Regulatory requirements |
| Security incident data | 3 years | Legal hold requirements |
| Behavioral analytics | 30 days | Operational necessity only |

---

## 5. Employee Rights (LGPD / GDPR)

Employees have the following rights regarding their personal data:

- **Right of Access**: Request a copy of all personal data we hold about you
- **Right to Rectification**: Request correction of inaccurate personal data
- **Right to Deletion**: Request deletion of personal data (subject to legal retention requirements)
- **Right to Data Portability**: Receive your data in a portable format
- **Right to Object**: Object to processing based on legitimate interests
- **Right to Restriction**: Request restriction of processing during disputes

**To exercise your rights**, contact: privacy@company.com

---

## 6. BYOD (Bring Your Own Device) Policy

For personally-owned devices enrolled in the platform:

- A **separate, sandboxed container** is used for corporate data
- The agent **only monitors corporate-related activities** within the corporate container
- Personal applications, files, and browsing remain completely private
- **You may unenroll your personal device at any time** through the self-service portal
- Upon unenrollment, all corporate data is wiped from the device container

---

## 7. Session Recording

Session recording is **disabled by default** and requires:
- Explicit legal justification
- Individual employee notification (minimum 72 hours notice)
- Written employee consent for ongoing recording
- Compliance with applicable labor laws

---

## 8. Third-Party Integrations

The platform integrates with:
| Service | Purpose | Data Shared |
|---------|---------|-------------|
| Microsoft Entra ID | Identity verification | User ID, group memberships |
| Google Workspace | Identity verification | User ID, group memberships |
| Tailscale/Headscale | VPN connectivity | Device certificates (no personal data) |

We do not sell personal data to third parties.

---

## 9. Security Measures

To protect employee data, we implement:
- End-to-end encryption for all data in transit (TLS 1.3)
- AES-256 encryption for all data at rest
- Role-based access control for admin access to logs
- Regular security audits and penetration testing
- Incident response procedures aligned with LGPD/GDPR notification requirements

---

## 10. Contact

**Privacy Officer**: privacy@company.com  
**Data Protection Officer**: dpo@company.com  
**Security Team**: security@company.com

For LGPD/GDPR inquiries: Within 15 business days of receipt of request.
