import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Info, CheckCircle } from 'lucide-react';

export interface SecurityEvent {
  id: string;
  type: 'alert' | 'info' | 'success';
  message: string;
  time: string;
  severity: 'critical' | 'high' | 'low' | 'info';
}

const severityConfig = {
  critical: { color: 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300', label: 'Critical' },
  high: { color: 'bg-orange-100 text-orange-700 dark:bg-orange-900 dark:text-orange-300', label: 'High' },
  low: { color: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300', label: 'Low' },
  info: { color: 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300', label: 'Info' },
};

const typeIcon = {
  alert: AlertTriangle,
  info: Info,
  success: CheckCircle,
};

export function SecurityEventsFeed({ events }: { events: SecurityEvent[] }) {
  return (
    <ul className="space-y-3">
      {events.map((event) => {
        const Icon = typeIcon[event.type];
        const severity = severityConfig[event.severity];
        return (
          <li key={event.id} className="flex items-start gap-3">
            <Icon className="mt-0.5 h-4 w-4 flex-shrink-0 text-muted-foreground" />
            <div className="min-w-0 flex-1">
              <p className="text-sm leading-tight">{event.message}</p>
              <div className="mt-1 flex items-center gap-2">
                <span className="text-xs text-muted-foreground">{event.time}</span>
                <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${severity.color}`}>
                  {severity.label}
                </span>
              </div>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
