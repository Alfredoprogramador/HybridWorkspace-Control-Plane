/**
 * Zero Trust architecture constants and configuration.
 * Based on NIST 800-207 Zero Trust Architecture principles.
 */

/** Zero Trust pillars to verify continuously */
export const ZERO_TRUST_PILLARS = [
  'identity',
  'device',
  'network',
  'application',
  'data',
] as const;

export type ZeroTrustPillar = (typeof ZERO_TRUST_PILLARS)[number];

/** Minimum compliance score to grant TRUSTED status */
export const TRUST_THRESHOLD_TRUSTED = 90;

/** Minimum compliance score for CONDITIONAL access */
export const TRUST_THRESHOLD_CONDITIONAL = 60;

/** Default token expiry for device agents (hours) */
export const DEVICE_TOKEN_EXPIRY_HOURS = 24;

/** How often device posture should be re-verified (minutes) */
export const POSTURE_CHECK_INTERVAL_MINUTES = 15;

/** Maximum failed verification attempts before blocking */
export const MAX_FAILED_VERIFICATIONS = 3;

/** Supported SSO providers */
export const SSO_PROVIDERS = ['microsoft', 'google', 'saml', 'oidc'] as const;

export type SSOProvider = (typeof SSO_PROVIDERS)[number];
