'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Monitor,
  Shield,
  Users,
  Settings,
  Activity,
  Lock,
  Network,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Devices', href: '/devices', icon: Monitor },
  { name: 'Policies', href: '/policies', icon: Shield },
  { name: 'Users', href: '/users', icon: Users },
  { name: 'Network', href: '/network', icon: Network },
  { name: 'Security Events', href: '/events', icon: Activity },
  { name: 'Zero Trust', href: '/zero-trust', icon: Lock },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-full w-64 flex-col border-r bg-card">
      {/* Logo */}
      <div className="flex h-16 items-center gap-2 border-b px-6">
        <Shield className="h-8 w-8 text-primary" />
        <div>
          <p className="text-sm font-bold leading-none">HybridWorkspace</p>
          <p className="text-xs text-muted-foreground">Control Plane</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <item.icon className="h-4 w-4 flex-shrink-0" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* User section */}
      <div className="border-t p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground font-semibold">
            AD
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium">Admin User</p>
            <p className="truncate text-xs text-muted-foreground">admin@org.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
