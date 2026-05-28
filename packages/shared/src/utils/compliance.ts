/**
 * Compliance score calculation utilities.
 */
import type { DevicePosture, DeviceTrustLevel } from '../types/device';

export const COMPLIANCE_WEIGHTS = {
  diskEncrypted: 25,
  antivirusEnabled: 20,
  osUpToDate: 20,
  firewallEnabled: 20,
  screenLockEnabled: 15,
} as const;

export function calculateComplianceScore(posture: DevicePosture): number {
  let score = 0;
  if (posture.diskEncrypted) score += COMPLIANCE_WEIGHTS.diskEncrypted;
  if (posture.antivirusEnabled) score += COMPLIANCE_WEIGHTS.antivirusEnabled;
  if (posture.osUpToDate) score += COMPLIANCE_WEIGHTS.osUpToDate;
  if (posture.firewallEnabled) score += COMPLIANCE_WEIGHTS.firewallEnabled;
  if (posture.screenLockEnabled) score += COMPLIANCE_WEIGHTS.screenLockEnabled;
  return score;
}

export function getTrustLevel(complianceScore: number): DeviceTrustLevel {
  if (complianceScore >= 90) return 'trusted';
  if (complianceScore >= 60) return 'conditional';
  return 'untrusted';
}

export function isDeviceCompliant(posture: DevicePosture): boolean {
  return calculateComplianceScore(posture) >= 80;
}
