import type { Metadata } from 'next';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { DeviceList } from '@/components/devices/DeviceList';

export const metadata: Metadata = {
  title: 'Devices – HybridWorkspace Control Plane',
};

export default function DevicesPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Devices</h1>
          <p className="text-muted-foreground">
            Manage and monitor device posture across your organization.
          </p>
        </div>
        <DeviceList />
      </div>
    </DashboardLayout>
  );
}
