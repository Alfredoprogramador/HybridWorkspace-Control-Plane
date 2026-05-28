/**
 * Policy-related TypeScript types.
 */

export type PolicyType = 'access' | 'device_compliance' | 'network' | 'data_protection' | 'behavioral';

export type PolicyEffect = 'allow' | 'deny' | 'conditional';

export type PolicyStatus = 'active' | 'inactive' | 'draft';

export interface PolicySubjects {
  users?: string[];
  groups?: string[];
  roles?: string[];
}

export interface PolicyResources {
  types?: string[];
  paths?: string[];
  services?: string[];
}

export interface PolicyConditions {
  trustLevels?: string[];
  networks?: string[];
  timeRanges?: Array<{ start: string; end: string; timezone: string }>;
  locations?: string[];
}

export interface Policy {
  id: string;
  name: string;
  description?: string;
  policyType: PolicyType;
  effect: PolicyEffect;
  status: PolicyStatus;
  priority: number;
  rules: Record<string, unknown>;
  subjects?: PolicySubjects;
  resources?: PolicyResources;
  conditions?: PolicyConditions;
  regoPolicy?: string;
  isSystem: boolean;
  version: number;
  createdById?: string;
  createdAt: string;
  updatedAt: string;
}

export interface PolicyEvaluationRequest {
  subject: Record<string, unknown>;
  resource: Record<string, unknown>;
  action: string;
  context?: Record<string, unknown>;
}

export interface PolicyEvaluationResult {
  allowed: boolean;
  policyId?: string;
  policyName?: string;
  reason?: string;
  conditionsMet: string[];
  conditionsFailed: string[];
}
