/**
 * User-related TypeScript types.
 */

export type UserRole = 'admin' | 'security_analyst' | 'it_manager' | 'employee';

export type AuthProvider = 'local' | 'microsoft' | 'google' | 'saml';

export interface User {
  id: string;
  email: string;
  username: string;
  fullName?: string;
  role: UserRole;
  authProvider: AuthProvider;
  department?: string;
  location?: string;
  isActive: boolean;
  isMfaEnabled: boolean;
  lastLoginAt?: string;
  createdAt: string;
}

export interface TokenResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
}
