import Cookies from 'js-cookie';
import { api } from './api';
import type { AuthTokens, AuthUser, LoginCredentials } from '@/types';

const COOKIE_OPTS = { secure: true, sameSite: 'strict' as const };

export async function login(credentials: LoginCredentials): Promise<AuthUser> {
  const form = new URLSearchParams();
  form.append('username', credentials.username);
  form.append('password', credentials.password);

  const { data } = await api.post<AuthTokens>('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

  Cookies.set('access_token', data.access_token, COOKIE_OPTS);
  Cookies.set('refresh_token', data.refresh_token, COOKIE_OPTS);

  return getMe();
}

export async function getMe(): Promise<AuthUser> {
  const { data } = await api.get<AuthUser>('/auth/me');
  return data;
}

export function logout(): void {
  Cookies.remove('access_token');
  Cookies.remove('refresh_token');
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
}

export function isAuthenticated(): boolean {
  return !!Cookies.get('access_token');
}
