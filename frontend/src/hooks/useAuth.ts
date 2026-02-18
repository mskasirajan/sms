'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { getMe, logout as doLogout, isAuthenticated } from '@/lib/auth';
import type { AuthUser } from '@/types';

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      setLoading(false);
      router.replace('/login');
      return;
    }
    getMe()
      .then(setUser)
      .catch(() => {
        doLogout();
      })
      .finally(() => setLoading(false));
  }, [router]);

  const logout = useCallback(() => {
    doLogout();
  }, []);

  return { user, loading, logout };
}
