'use client';

import { Sidebar } from '@/components/layout/Sidebar';
import { useAuth } from '@/hooks/useAuth';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, loading, logout } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm text-gray-500">Loading…</span>
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar user={user} onLogout={logout} />
      <div className="flex-1 flex flex-col min-w-0">{children}</div>
    </div>
  );
}
