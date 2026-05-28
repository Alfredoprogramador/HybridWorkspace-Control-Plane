/**
 * Zero Trust policy engine – client-side helper for evaluating access decisions.
 */
import type {
  PolicyEvaluationRequest,
  PolicyEvaluationResult,
  Device,
  DeviceTrustLevel,
} from '@hwcp/shared';
import {
  TRUST_THRESHOLD_TRUSTED,
  TRUST_THRESHOLD_CONDITIONAL,
} from '@hwcp/shared';

export interface ZeroTrustContext {
  userId: string;
  userRole: string;
  userGroups: string[];
  device?: Device;
  networkType?: 'corporate' | 'public' | 'vpn' | 'unknown';
  location?: string;
}

/**
 * Build a PolicyEvaluationRequest from a Zero Trust context.
 */
export function buildEvaluationRequest(
  ctx: ZeroTrustContext,
  resource: { type: string; id?: string },
  action: string
): PolicyEvaluationRequest {
  const trustLevel: DeviceTrustLevel = ctx.device?.trustLevel ?? 'untrusted';

  return {
    subject: {
      id: ctx.userId,
      role: ctx.userRole,
      groups: ctx.userGroups,
      device_trust: trustLevel,
      device_compliant: ctx.device?.isCompliant ?? false,
    },
    resource: {
      type: resource.type,
      id: resource.id,
    },
    action,
    context: {
      network_type: ctx.networkType ?? 'unknown',
      location: ctx.location,
      timestamp: new Date().toISOString(),
    },
  };
}

/**
 * Quick local trust level check based on device compliance score.
 * Use as a fast pre-check before calling the backend policy API.
 */
export function quickTrustCheck(
  complianceScore: number
): DeviceTrustLevel {
  if (complianceScore >= TRUST_THRESHOLD_TRUSTED) return 'trusted';
  if (complianceScore >= TRUST_THRESHOLD_CONDITIONAL) return 'conditional';
  return 'untrusted';
}

/**
 * Determine if an access request should be blocked immediately based on
 * the Zero Trust principle of least privilege.
 */
export function shouldDenyImmediately(ctx: ZeroTrustContext): boolean {
  if (!ctx.device) return true;
  if (ctx.device.trustLevel === 'blocked' || ctx.device.status === 'revoked') return true;
  if (!ctx.device.isCompliant && ctx.networkType === 'public') return true;
  return false;
}
