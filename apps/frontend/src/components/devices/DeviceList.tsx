'use client';

import { Monitor, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
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

const mockDevices = [
  {
    id: '1',
    name: 'MBP-John-001',
    hostname: 'johns-macbook-pro',
    os: 'macOS 14.1',
    owner: 'john.doe@org.com',
    trustLevel: 'trusted',
    complianceScore: 95,
    lastSeen: '2 min ago',
    status: 'online',
  },
  {
    id: '2',
    name: 'WIN-Sales-042',
    hostname: 'win-sales-042',
    os: 'Windows 11 22H2',
    owner: 'jane.smith@org.com',
    trustLevel: 'conditional',
    complianceScore: 65,
    lastSeen: '1 hour ago',
    status: 'online',
  },
  {
    id: '3',
    name: 'Linux-Dev-Sarah',
    hostname: 'sarah-dev-laptop',
    os: 'Ubuntu 24.04 LTS',
    owner: 'sarah.k@org.com',
    trustLevel: 'trusted',
    complianceScore: 100,
    lastSeen: '5 min ago',
    status: 'online',
  },
  {
    id: '4',
    name: 'iPad-Manager-001',
    hostname: 'ipad-manager-001',
    os: 'iPadOS 17.2',
    owner: 'manager@org.com',
    trustLevel: 'untrusted',
    complianceScore: 30,
    lastSeen: '3 days ago',
    status: 'offline',
  },
];

const trustBadge = {
  trusted: 'bg-green-100 text-green-700',
  conditional: 'bg-yellow-100 text-yellow-700',
  untrusted: 'bg-red-100 text-red-700',
};

const statusIcon = {
  online: <CheckCircle className="h-4 w-4 text-green-500" />,
  offline: <XCircle className="h-4 w-4 text-gray-400" />,
};

export function DeviceList() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <Monitor className="h-5 w-5" />
          Enrolled Devices
        </CardTitle>
        <Button size="sm">Enroll Device</Button>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Device</TableHead>
              <TableHead>OS</TableHead>
              <TableHead>Owner</TableHead>
              <TableHead>Trust Level</TableHead>
              <TableHead>Compliance</TableHead>
              <TableHead>Last Seen</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="w-[80px]">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {mockDevices.map((device) => (
              <TableRow key={device.id}>
                <TableCell>
                  <div>
                    <p className="font-medium">{device.name}</p>
                    <p className="text-xs text-muted-foreground">{device.hostname}</p>
                  </div>
                </TableCell>
                <TableCell className="text-sm">{device.os}</TableCell>
                <TableCell className="text-sm">{device.owner}</TableCell>
                <TableCell>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold capitalize ${trustBadge[device.trustLevel as keyof typeof trustBadge]}`}
                  >
                    {device.trustLevel}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-16 rounded-full bg-muted overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          device.complianceScore >= 80
                            ? 'bg-green-500'
                            : device.complianceScore >= 60
                              ? 'bg-yellow-500'
                              : 'bg-red-500'
                        }`}
                        style={{ width: `${device.complianceScore}%` }}
                      />
                    </div>
                    <span className="text-xs">{device.complianceScore}%</span>
                  </div>
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">{device.lastSeen}</TableCell>
                <TableCell>
                  <div className="flex items-center gap-1">
                    {statusIcon[device.status as keyof typeof statusIcon]}
                    <span className="text-xs capitalize">{device.status}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <Button variant="ghost" size="sm">
                    View
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
