/**
 * Device-related TypeScript types shared across frontend, desktop agent, and backend.
 */

export type DeviceOS = 'windows' | 'macos' | 'linux' | 'ios' | 'android';

export type DeviceTrustLevel = 'trusted' | 'conditional' | 'untrusted' | 'blocked';

export type DeviceStatus = 'online' | 'offline' | 'enrolled' | 'pending' | 'revoked';

export interface DevicePosture {
  diskEncrypted: boolean;
  antivirusEnabled: boolean;
  osUpToDate: boolean;
  firewallEnabled: boolean;
  screenLockEnabled: boolean;
  osVersion?: string;
}

export interface Device {
  id: string;
  name: string;
  hostname: string;
  serialNumber?: string;
  osType: DeviceOS;
  osVersion?: string;
  agentVersion?: string;
  trustLevel: DeviceTrustLevel;
  status: DeviceStatus;
  isCompliant: boolean;
  complianceScore?: number;
  posture: DevicePosture;
  ipAddress?: string;
  tailscaleIp?: string;
  macAddress?: string;
  ownerId?: string;
  lastSeenAt?: string;
  enrolledAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface DeviceList {
  items: Device[];
  total: number;
  page: number;
  pageSize: number;
}
