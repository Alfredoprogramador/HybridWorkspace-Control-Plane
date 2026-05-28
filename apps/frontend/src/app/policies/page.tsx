import type { Metadata } from 'next';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { PolicyList } from '@/components/policies/PolicyList';

export const metadata: Metadata = {
  title: 'Policies – HybridWorkspace Control Plane',
};

export default function PoliciesPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Access Policies</h1>
          <p className="text-muted-foreground">
            Define and manage Zero Trust access policies for your organization.
          </p>
        </div>
        <PolicyList />
      </div>
    </DashboardLayout>
  );
}
