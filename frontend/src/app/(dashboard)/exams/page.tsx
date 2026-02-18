'use client';

import { useEffect, useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { PlusIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Table, Thead, Tbody, Th, Td, Tr, EmptyRow } from '@/components/ui/Table';
import { Modal } from '@/components/ui/Modal';
import { api, getErrorMessage } from '@/lib/api';
import type { Exam, ExamSchedule, Mark, MarksUpload } from '@/types';

interface ExamCreate {
  name: string;
  exam_type: string;
  start_date: string;
  end_date: string;
}

export default function ExamsPage() {
  const [exams, setExams]             = useState<Exam[]>([]);
  const [selectedExam, setSelected]   = useState<Exam | null>(null);
  const [schedules, setSchedules]     = useState<ExamSchedule[]>([]);
  const [marks, setMarks]             = useState<Mark[]>([]);
  const [selectedSched, setSelSched]  = useState<ExamSchedule | null>(null);
  const [examModal, setExamModal]     = useState(false);
  const [marksModal, setMarksModal]   = useState(false);
  const [loading, setLoading]         = useState(false);
  const [saving, setSaving]           = useState(false);

  const examForm  = useForm<ExamCreate>();
  const marksForm = useForm<{ records: { student_id: number; marks_obtained: number }[] }>();

  const fetchExams = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<Exam[]>('/exams');
      setExams(Array.isArray(data) ? data : (data as { items: Exam[] }).items ?? []);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchExams(); }, [fetchExams]);

  const selectExam = async (exam: Exam) => {
    setSelected(exam);
    setSchedules([]);
    try {
      const { data } = await api.get<ExamSchedule[]>(`/exams/${exam.id}/schedule`);
      setSchedules(Array.isArray(data) ? data : []);
    } catch { /* silent */ }
  };

  const openMarks = async (sched: ExamSchedule) => {
    setSelSched(sched);
    try {
      const { data } = await api.get<Mark[]>(`/exams/marks?exam_schedule_id=${sched.id}`);
      setMarks(Array.isArray(data) ? data : []);
    } catch { setMarks([]); }
    setMarksModal(true);
  };

  const submitExam = async (data: ExamCreate) => {
    setSaving(true);
    try {
      await api.post('/exams/create', data);
      toast.success('Exam created');
      setExamModal(false);
      fetchExams();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const submitMarks = async () => {
    if (!selectedSched) return;
    setSaving(true);
    try {
      const payload: MarksUpload = {
        exam_schedule_id: selectedSched.id,
        records: marks.map((m) => ({ student_id: m.student_id, marks_obtained: m.marks_obtained })),
      };
      await api.post('/exams/marks/upload', payload);
      toast.success('Marks saved');
      setMarksModal(false);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <Header title="Exams" subtitle="Manage exams, schedules and marks" />
      <main className="flex-1 p-6 space-y-4">

        {/* Exam list */}
        <Card padding={false}>
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
            <span className="font-semibold text-gray-700">All Exams</span>
            <Button size="sm" onClick={() => { examForm.reset(); setExamModal(true); }}>
              <PlusIcon className="h-4 w-4" /> New Exam
            </Button>
          </div>
          <Table>
            <Thead>
              <tr>
                <Th>Name</Th>
                <Th>Type</Th>
                <Th>Start Date</Th>
                <Th>End Date</Th>
                <Th>Status</Th>
                <Th></Th>
              </tr>
            </Thead>
            <Tbody>
              {loading ? (
                <tr><td colSpan={6} className="text-center py-8 text-gray-400 text-sm">Loading…</td></tr>
              ) : exams.length === 0 ? (
                <EmptyRow colSpan={6} />
              ) : (
                exams.map((e) => (
                  <Tr key={e.id} onClick={() => selectExam(e)}>
                    <Td className="font-medium">{e.name}</Td>
                    <Td>{e.exam_type}</Td>
                    <Td>{e.start_date}</Td>
                    <Td>{e.end_date}</Td>
                    <Td>
                      <Badge variant={e.is_active ? 'success' : 'neutral'}>
                        {e.is_active ? 'Active' : 'Closed'}
                      </Badge>
                    </Td>
                    <Td><ChevronRightIcon className="h-4 w-4 text-gray-400" /></Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>
        </Card>

        {/* Schedule for selected exam */}
        {selectedExam && (
          <Card padding={false}>
            <div className="px-4 py-3 border-b border-gray-200">
              <span className="font-semibold text-gray-700">
                Schedule — {selectedExam.name}
              </span>
            </div>
            <Table>
              <Thead>
                <tr>
                  <Th>Subject</Th>
                  <Th>Date</Th>
                  <Th>Time</Th>
                  <Th>Max Marks</Th>
                  <Th>Pass Marks</Th>
                  <Th>Action</Th>
                </tr>
              </Thead>
              <Tbody>
                {schedules.length === 0 ? (
                  <EmptyRow colSpan={6} message="No schedule entries found" />
                ) : (
                  schedules.map((s) => (
                    <Tr key={s.id}>
                      <Td className="font-medium">{s.subject_name}</Td>
                      <Td>{s.exam_date}</Td>
                      <Td>{s.start_time} – {s.end_time}</Td>
                      <Td>{s.max_marks}</Td>
                      <Td>{s.pass_marks}</Td>
                      <Td>
                        <Button size="sm" variant="secondary" onClick={() => openMarks(s)}>
                          Enter Marks
                        </Button>
                      </Td>
                    </Tr>
                  ))
                )}
              </Tbody>
            </Table>
          </Card>
        )}
      </main>

      {/* Create Exam Modal */}
      <Modal open={examModal} onClose={() => setExamModal(false)} title="Create Exam">
        <form onSubmit={examForm.handleSubmit(submitExam)} className="space-y-4">
          <Input label="Exam Name" error={examForm.formState.errors.name?.message} {...examForm.register('name', { required: 'Required' })} />
          <Select
            label="Exam Type"
            options={[
              { value: 'Unit Test', label: 'Unit Test' },
              { value: 'Mid Term',  label: 'Mid Term' },
              { value: 'Final',     label: 'Final' },
              { value: 'Monthly',   label: 'Monthly' },
            ]}
            placeholder="Select type"
            error={examForm.formState.errors.exam_type?.message}
            {...examForm.register('exam_type', { required: 'Required' })}
          />
          <Input label="Start Date" type="date" error={examForm.formState.errors.start_date?.message} {...examForm.register('start_date', { required: 'Required' })} />
          <Input label="End Date"   type="date" error={examForm.formState.errors.end_date?.message}   {...examForm.register('end_date',   { required: 'Required' })} />
          <div className="flex justify-end gap-3 pt-2">
            <Button variant="secondary" type="button" onClick={() => setExamModal(false)}>Cancel</Button>
            <Button type="submit" loading={saving}>Create Exam</Button>
          </div>
        </form>
      </Modal>

      {/* Enter Marks Modal */}
      <Modal
        open={marksModal}
        onClose={() => setMarksModal(false)}
        title={`Marks — ${selectedSched?.subject_name}`}
        size="lg"
      >
        <div className="space-y-3">
          <p className="text-sm text-gray-500">Max Marks: {selectedSched?.max_marks} | Pass: {selectedSched?.pass_marks}</p>
          <Table>
            <Thead>
              <tr>
                <Th>Student</Th>
                <Th>Admission No.</Th>
                <Th>Marks</Th>
                <Th>Grade</Th>
              </tr>
            </Thead>
            <Tbody>
              {marks.length === 0 ? (
                <EmptyRow colSpan={4} message="No students loaded" />
              ) : (
                marks.map((m, idx) => (
                  <Tr key={m.student_id}>
                    <Td>{m.student_name}</Td>
                    <Td className="font-mono text-xs">{m.admission_number}</Td>
                    <Td>
                      <input
                        type="number"
                        min={0}
                        max={selectedSched?.max_marks}
                        value={m.marks_obtained}
                        onChange={(e) => {
                          const v = Number(e.target.value);
                          setMarks((prev) => prev.map((r, i) => i === idx ? { ...r, marks_obtained: v } : r));
                        }}
                        className="w-20 border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </Td>
                    <Td>
                      <Badge variant={m.is_pass ? 'success' : 'danger'}>{m.grade}</Badge>
                    </Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>
          <div className="flex justify-end gap-3 pt-2">
            <Button variant="secondary" onClick={() => setMarksModal(false)}>Cancel</Button>
            <Button onClick={submitMarks} loading={saving}>Save Marks</Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
