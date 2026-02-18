'use client';

import { useEffect, useState } from 'react';
import {
  UserGroupIcon,
  AcademicCapIcon,
  ClipboardDocumentCheckIcon,
  BanknotesIcon,
} from '@heroicons/react/24/outline';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, Legend,
} from 'recharts';
import { Header } from '@/components/layout/Header';
import { StatCard, Card, CardHeader, CardTitle } from '@/components/ui/Card';
import { api } from '@/lib/api';

interface DashboardStats {
  total_students: number;
  total_teachers: number;
  today_attendance_pct: number;
  pending_fees_count: number;
  attendance_trend: { day: string; present: number; absent: number }[];
  fee_collection: { month: string; collected: number; pending: number }[];
}

const MOCK_STATS: DashboardStats = {
  total_students: 842,
  total_teachers: 56,
  today_attendance_pct: 91,
  pending_fees_count: 38,
  attendance_trend: [
    { day: 'Mon', present: 780, absent: 62 },
    { day: 'Tue', present: 795, absent: 47 },
    { day: 'Wed', present: 812, absent: 30 },
    { day: 'Thu', present: 769, absent: 73 },
    { day: 'Fri', present: 800, absent: 42 },
  ],
  fee_collection: [
    { month: 'Sep', collected: 420000, pending: 80000 },
    { month: 'Oct', collected: 510000, pending: 60000 },
    { month: 'Nov', collected: 490000, pending: 90000 },
    { month: 'Dec', collected: 530000, pending: 40000 },
    { month: 'Jan', collected: 480000, pending: 70000 },
  ],
};

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>(MOCK_STATS);

  useEffect(() => {
    api.get<DashboardStats>('/dashboard/stats')
      .then((r) => setStats(r.data))
      .catch(() => { /* fall back to mock */ });
  }, []);

  return (
    <>
      <Header title="Dashboard" subtitle="Welcome back — here's what's happening today" />
      <main className="flex-1 p-6 space-y-6">

        {/* Stat Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <StatCard
            title="Total Students"
            value={stats.total_students.toLocaleString()}
            icon={<UserGroupIcon className="h-6 w-6" />}
            color="blue"
          />
          <StatCard
            title="Total Teachers"
            value={stats.total_teachers}
            icon={<AcademicCapIcon className="h-6 w-6" />}
            color="green"
          />
          <StatCard
            title="Today Attendance"
            value={`${stats.today_attendance_pct}%`}
            icon={<ClipboardDocumentCheckIcon className="h-6 w-6" />}
            color="purple"
          />
          <StatCard
            title="Pending Fees"
            value={stats.pending_fees_count}
            icon={<BanknotesIcon className="h-6 w-6" />}
            color="yellow"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Weekly Attendance</CardTitle>
            </CardHeader>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={stats.attendance_trend}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="present" fill="#6366f1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="absent"  fill="#f87171" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Fee Collection (₹)</CardTitle>
            </CardHeader>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={stats.fee_collection}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
                <Tooltip formatter={(v: number) => `₹${v.toLocaleString()}`} />
                <Legend />
                <Line type="monotone" dataKey="collected" stroke="#6366f1" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="pending"   stroke="#fb923c" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </div>

      </main>
    </>
  );
}
