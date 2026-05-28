'use client';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const data = [
  { date: 'Nov 22', compliant: 78, non_compliant: 22 },
  { date: 'Nov 29', compliant: 80, non_compliant: 20 },
  { date: 'Dec 06', compliant: 83, non_compliant: 17 },
  { date: 'Dec 13', compliant: 85, non_compliant: 15 },
  { date: 'Dec 20', compliant: 84, non_compliant: 16 },
  { date: 'Dec 27', compliant: 87, non_compliant: 13 },
  { date: 'Jan 03', compliant: 87, non_compliant: 13 },
];

export function ComplianceChart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Device Compliance Trend (%)</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Area
              type="monotone"
              dataKey="compliant"
              stackId="1"
              stroke="#22c55e"
              fill="#22c55e"
              fillOpacity={0.3}
              name="Compliant"
            />
            <Area
              type="monotone"
              dataKey="non_compliant"
              stackId="2"
              stroke="#ef4444"
              fill="#ef4444"
              fillOpacity={0.3}
              name="Non-compliant"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
