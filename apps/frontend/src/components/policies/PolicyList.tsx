'use client';

import { Shield, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const mockPolicies = [
  {
    id: '1',
    name: 'Zero Trust Remote Access',
    type: 'access',
    effect: 'allow',
    status: 'active',
    priority: 10,
    description: 'Allow remote access for verified corporate devices',
    updated: '2024-12-28',
  },
  {
    id: '2',
    name: 'Block Untrusted Devices',
    type: 'access',
    effect: 'deny',
    status: 'active',
    priority: 5,
    description: 'Deny access from devices with untrusted posture',
    updated: '2024-12-20',
  },
  {
    id: '3',
    name: 'Engineering Full Access',
    type: 'access',
    effect: 'allow',
    status: 'active',
    priority: 20,
    description: 'Engineering team full access to dev resources',
    updated: '2024-11-15',
  },
  {
    id: '4',
    name: 'Device Compliance Requirements',
    type: 'device_compliance',
    effect: 'conditional',
    status: 'active',
    priority: 1,
    description: 'Enforce disk encryption, AV, and OS updates',
    updated: '2024-12-01',
  },
];

const effectBadge = {
  allow: 'bg-green-100 text-green-700',
  deny: 'bg-red-100 text-red-700',
  conditional: 'bg-yellow-100 text-yellow-700',
};

const statusBadge = {
  active: 'bg-blue-100 text-blue-700',
  inactive: 'bg-gray-100 text-gray-700',
  draft: 'bg-purple-100 text-purple-700',
};

export function PolicyList() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          Access Policies
        </CardTitle>
        <Button size="sm" className="gap-1">
          <Plus className="h-4 w-4" />
          New Policy
        </Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Effect</TableHead>
              <TableHead>Priority</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Updated</TableHead>
              <TableHead className="w-[80px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {mockPolicies.map((policy) => (
              <TableRow key={policy.id}>
                <TableCell>
                  <div>
                    <p className="font-medium">{policy.name}</p>
                    <p className="text-xs text-muted-foreground">{policy.description}</p>
                  </div>
                </TableCell>
                <TableCell>
                  <span className="inline-flex items-center rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium capitalize">
                    {policy.type.replace('_', ' ')}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize ${effectBadge[policy.effect as keyof typeof effectBadge]}`}
                  >
                    {policy.effect}
                  </span>
                </TableCell>
                <TableCell className="text-sm font-mono">{policy.priority}</TableCell>
                <TableCell>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${statusBadge[policy.status as keyof typeof statusBadge]}`}
                  >
                    {policy.status}
                  </span>
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">{policy.updated}</TableCell>
                <TableCell>
                  <Button variant="ghost" size="sm">
                    Edit
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}
