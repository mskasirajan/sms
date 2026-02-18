'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import clsx from 'clsx';
import {
  HomeIcon,
  UserGroupIcon,
  AcademicCapIcon,
  ClipboardDocumentCheckIcon,
  BanknotesIcon,
  DocumentTextIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';
import type { AuthUser } from '@/types';

interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  roles?: string[];
}

const navItems: NavItem[] = [
  { href: '/dashboard',  label: 'Dashboard',  icon: HomeIcon },
  { href: '/students',   label: 'Students',   icon: UserGroupIcon, roles: ['school_admin', 'principal', 'teacher'] },
  { href: '/teachers',   label: 'Teachers',   icon: AcademicCapIcon, roles: ['school_admin', 'principal'] },
  { href: '/attendance', label: 'Attendance', icon: ClipboardDocumentCheckIcon, roles: ['school_admin', 'principal', 'teacher'] },
  { href: '/fees',       label: 'Fees',       icon: BanknotesIcon, roles: ['school_admin', 'accountant'] },
  { href: '/exams',      label: 'Exams',      icon: DocumentTextIcon, roles: ['school_admin', 'principal', 'teacher'] },
];

interface SidebarProps {
  user: AuthUser;
  onLogout: () => void;
}

export function Sidebar({ user, onLogout }: SidebarProps) {
  const pathname = usePathname();

  const visibleItems = navItems.filter(
    (item) => !item.roles || item.roles.includes(user.role)
  );

  return (
    <aside className="flex flex-col w-64 min-h-screen bg-gray-900 text-gray-100">
      {/* Logo */}
      <div className="px-6 py-5 border-b border-gray-800">
        <span className="text-xl font-bold text-white">
          <span className="text-primary-400">SMS</span> Portal
        </span>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {visibleItems.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                active
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              )}
            >
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* User + Logout */}
      <div className="px-4 py-4 border-t border-gray-800">
        <div className="flex items-center gap-3 mb-3">
          <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-sm font-semibold">
            {(user.full_name ?? user.email ?? '?').charAt(0).toUpperCase()}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-white truncate">{user.full_name ?? user.email}</p>
            <p className="text-xs text-gray-400 capitalize">{(user.role ?? '').replace(/_/g, ' ')}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
        >
          <ArrowRightOnRectangleIcon className="h-4 w-4" />
          Sign out
        </button>
      </div>
    </aside>
  );
}
