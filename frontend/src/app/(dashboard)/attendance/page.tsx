'use client';

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { CheckIcon } from '@heroicons/react/24/outline';
import { Header } from '@/components/layout/Header';
import { Card, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Input';
import { Table, Thead, Tbody, Th, Td, Tr, EmptyRow } from '@/components/ui/Table';
import { attendanceBadge } from '@/components/ui/Badge';
import { api, getErrorMessage } from '@/lib/api';
import type { Class, Student, AttendanceStatus, AttendanceMarkRequest, AttendanceReport } from '@/types';

interface AttendanceRow {
  student_id: number;
  full_name: string;
  admission_number: string;
  status: AttendanceStatus;
}

export default function AttendancePage() {
  const [classes, setClasses]     = useState<Class[]>([]);
  const [classId, setClassId]     = useState('');
  const [date, setDate]           = useState(new Date().toISOString().split('T')[0]);
  const [rows, setRows]           = useState<AttendanceRow[]>([]);
  const [report, setReport]       = useState<AttendanceReport[]>([]);
  const [tab, setTab]             = useState<'mark' | 'report'>('mark');
  const [saving, setSaving]       = useState(false);
  const [loadingStudents, setLS]  = useState(false);

  useEffect(() => {
    api.get<Class[]>('/classes').then((r) => setClasses(r.data)).catch(() => {});
  }, []);

  const loadStudents = async () => {
    if (!classId) return toast.error('Select a class first');
    setLS(true);
    try {
      const { data } = await api.get<Student[]>(`/students?class_id=${classId}&size=200`);
      const students = Array.isArray(data) ? data : (data as { items: Student[] }).items;
      setRows(students.map((s) => ({
        student_id: s.id,
        full_name: s.full_name,
        admission_number: s.admission_number,
        status: 'Present' as AttendanceStatus,
      })));
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLS(false);
    }
  };

  const toggleStatus = (idx: number, status: AttendanceStatus) => {
    setRows((prev) => prev.map((r, i) => (i === idx ? { ...r, status } : r)));
  };

  const markAll = (status: AttendanceStatus) => {
    setRows((prev) => prev.map((r) => ({ ...r, status })));
  };

  const submitAttendance = async () => {
    if (!rows.length) return toast.error('No students loaded');
    setSaving(true);
    try {
      const payload: AttendanceMarkRequest = {
        class_id: Number(classId),
        session_date: date,
        records: rows.map((r) => ({ student_id: r.student_id, status: r.status })),
      };
      await api.post('/attendance/mark', payload);
      toast.success('Attendance saved successfully');
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const loadReport = async () => {
    if (!classId) return toast.error('Select a class first');
    try {
      const { data } = await api.get<AttendanceReport[]>('/attendance/report', {
        params: { class_id: classId },
      });
      setReport(data);
      setTab('report');
    } catch (err) {
      toast.error(getErrorMessage(err));
    }
  };

  const STATUSES: AttendanceStatus[] = ['Present', 'Absent', 'Late', 'Half-Day'];
  const statusColor: Record<AttendanceStatus, string> = {
    Present:  'bg-green-100 text-green-700 border-green-300',
    Absent:   'bg-red-100 text-red-700 border-red-300',
    Late:     'bg-yellow-100 text-yellow-700 border-yellow-300',
    'Half-Day': 'bg-blue-100 text-blue-700 border-blue-300',
  };

  return (
    <>
      <Header title="Attendance" subtitle="Mark and track student attendance" />
      <main className="flex-1 p-6 space-y-4">

        {/* Filters */}
        <Card>
          <div className="flex flex-wrap items-end gap-4">
            <Select
              label="Class"
              options={classes.map((c) => ({ value: c.id, label: c.name }))}
              placeholder="Select class"
              value={classId}
              onChange={(e) => setClassId(e.target.value)}
              className="w-48"
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
              <input
                type="date"
                value={date}
                max={new Date().toISOString().split('T')[0]}
                onChange={(e) => setDate(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <Button onClick={loadStudents} loading={loadingStudents} variant="secondary">
              Load Students
            </Button>
            <Button onClick={loadReport} variant="secondary">
              View Report
            </Button>
          </div>
        </Card>

        {/* Tabs */}
        <div className="flex gap-2">
          {(['mark', 'report'] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                tab === t ? 'bg-primary-600 text-white' : 'bg-white border border-gray-300 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {t === 'mark' ? 'Mark Attendance' : 'Report'}
            </button>
          ))}
        </div>

        {/* Mark Attendance */}
        {tab === 'mark' && (
          <Card padding={false}>
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
              <span className="text-sm text-gray-600">{rows.length} students</span>
              <div className="flex gap-2">
                <Button size="sm" variant="secondary" onClick={() => markAll('Present')}>All Present</Button>
                <Button size="sm" variant="secondary" onClick={() => markAll('Absent')}>All Absent</Button>
                {rows.length > 0 && (
                  <Button size="sm" onClick={submitAttendance} loading={saving}>
                    <CheckIcon className="h-4 w-4" /> Save
                  </Button>
                )}
              </div>
            </div>
            <Table>
              <Thead>
                <tr>
                  <Th>#</Th>
                  <Th>Admission No.</Th>
                  <Th>Name</Th>
                  <Th>Status</Th>
                </tr>
              </Thead>
              <Tbody>
                {rows.length === 0 ? (
                  <EmptyRow colSpan={4} message="Load a class to start marking attendance" />
                ) : (
                  rows.map((r, idx) => (
                    <Tr key={r.student_id}>
                      <Td className="text-gray-400">{idx + 1}</Td>
                      <Td className="font-mono text-xs">{r.admission_number}</Td>
                      <Td className="font-medium">{r.full_name}</Td>
                      <Td>
                        <div className="flex gap-1 flex-wrap">
                          {STATUSES.map((s) => (
                            <button
                              key={s}
                              onClick={() => toggleStatus(idx, s)}
                              className={`px-2 py-0.5 rounded text-xs border font-medium transition-colors ${
                                r.status === s ? statusColor[s] : 'bg-gray-50 text-gray-400 border-gray-200 hover:border-gray-400'
                              }`}
                            >
                              {s}
                            </button>
                          ))}
                        </div>
                      </Td>
                    </Tr>
                  ))
                )}
              </Tbody>
            </Table>
          </Card>
        )}

        {/* Report */}
        {tab === 'report' && (
          <Card padding={false}>
            <Table>
              <Thead>
                <tr>
                  <Th>Student</Th>
                  <Th>Admission No.</Th>
                  <Th>Total Days</Th>
                  <Th>Present</Th>
                  <Th>Absent</Th>
                  <Th>Late</Th>
                  <Th>%</Th>
                </tr>
              </Thead>
              <Tbody>
                {report.length === 0 ? (
                  <EmptyRow colSpan={7} message="Select a class and click View Report" />
                ) : (
                  report.map((r) => (
                    <Tr key={r.student_id}>
                      <Td className="font-medium">{r.student_name}</Td>
                      <Td className="font-mono text-xs">{r.admission_number}</Td>
                      <Td>{r.total_days}</Td>
                      <Td className="text-green-600">{r.present}</Td>
                      <Td className="text-red-600">{r.absent}</Td>
                      <Td className="text-yellow-600">{r.late}</Td>
                      <Td>
                        {attendanceBadge(r.percentage >= 75 ? 'Present' : 'Absent')}
                        <span className="ml-1 text-xs text-gray-600">{r.percentage.toFixed(1)}%</span>
                      </Td>
                    </Tr>
                  ))
                )}
              </Tbody>
            </Table>
          </Card>
        )}

      </main>
    </>
  );
}
