'use client';

import { Monitor, Shield, Users, AlertTriangle, CheckCircle, Clock, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ComplianceChart } from './ComplianceChart';
import { SecurityEventsFeed } from './SecurityEventsFeed';
import type { SecurityEvent } from './SecurityEventsFeed';

const stats = [
  {
    title: 'Total Devices',
    value: '1,247',
    change: '+12 this week',
    icon: Monitor,
    color: 'text-blue-500',
  },
  {
    title: 'Compliant Devices',
    value: '1,089',
    change: '87.3% compliance',
    icon: CheckCircle,
    color: 'text-green-500',
  },
  {
    title: 'Active Users',
    value: '892',
    change: '+34 this month',
    icon: Users,
    color: 'text-purple-500',
  },
  {
    title: 'Security Alerts',
    value: '23',
    change: '-5 from yesterday',
    icon: AlertTriangle,
    color: 'text-orange-500',
  },
];

const recentEvents: SecurityEvent[] = [
  {
    id: '1',
    type: 'alert',
    message: 'Device "MBP-John-001" failed compliance check: disk not encrypted',
    time: '2 min ago',
    severity: 'high',
  },
  {
    id: '2',
    type: 'info',
    message: 'Policy "Remote Access - Engineering" updated by admin@org.com',
    time: '15 min ago',
    severity: 'low',
  },
  {
    id: '3',
    type: 'success',
    message: '47 devices passed continuous verification check',
    time: '1 hour ago',
    severity: 'info',
  },
  {
    id: '4',
    type: 'alert',
    message: 'Unusual login attempt from device "WIN-SALES-042" – blocked',
    time: '2 hours ago',
    severity: 'critical',
  },
  {
    id: '5',
    type: 'info',
    message: 'New device enrolled: "Linux-Dev-Sarah" (Ubuntu 24.04)',
    time: '3 hours ago',
    severity: 'low',
  },
];

export function DashboardOverview() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Zero Trust security posture overview for your organization.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground mt-1">{stat.change}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts + Events */}
      <div className="grid gap-4 md:grid-cols-2">
        <ComplianceChart />
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-4 w-4" />
              Security Events
            </CardTitle>
          </CardHeader>
          <CardContent>
            <SecurityEventsFeed events={recentEvents} />
          </CardContent>
        </Card>
      </div>

      {/* Zero Trust Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Zero Trust Verification Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-lg border p-4 text-center">
              <div className="text-2xl font-bold text-green-500">TRUSTED</div>
              <div className="text-3xl font-bold mt-1">743</div>
              <div className="text-sm text-muted-foreground">devices</div>
            </div>
            <div className="rounded-lg border p-4 text-center">
              <div className="text-2xl font-bold text-yellow-500">CONDITIONAL</div>
              <div className="text-3xl font-bold mt-1">346</div>
              <div className="text-sm text-muted-foreground">devices</div>
            </div>
            <div className="rounded-lg border p-4 text-center">
              <div className="text-2xl font-bold text-red-500">UNTRUSTED</div>
              <div className="text-3xl font-bold mt-1">158</div>
              <div className="text-sm text-muted-foreground">devices</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
