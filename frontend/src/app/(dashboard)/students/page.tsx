'use client';

import { useEffect, useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { PlusIcon, MagnifyingGlassIcon, PencilIcon } from '@heroicons/react/24/outline';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Table, Thead, Tbody, Th, Td, Tr, EmptyRow, Pagination } from '@/components/ui/Table';
import { Modal } from '@/components/ui/Modal';
import { api, getErrorMessage } from '@/lib/api';
import type { Student, StudentCreate, PaginatedResponse } from '@/types';

export default function StudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Student | null>(null);
  const [saving, setSaving] = useState(false);

  const PAGE_SIZE = 10;

  const { register, handleSubmit, reset, formState: { errors } } = useForm<StudentCreate>();

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<PaginatedResponse<Student>>('/students', {
        params: { page, size: PAGE_SIZE, search: search || undefined },
      });
      setStudents(data.items);
      setTotal(data.total);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchStudents(); }, [fetchStudents]);

  const openCreate = () => { setEditing(null); reset({}); setModalOpen(true); };
  const openEdit   = (s: Student) => {
    setEditing(s);
    reset({
      admission_number: s.admission_number,
      full_name: s.full_name,
      date_of_birth: s.date_of_birth,
      gender: s.gender,
      address: s.address,
      phone: s.phone,
      email: s.email,
    });
    setModalOpen(true);
  };

  const onSubmit = async (data: StudentCreate) => {
    setSaving(true);
    try {
      if (editing) {
        await api.put(`/students/${editing.id}`, data);
        toast.success('Student updated');
      } else {
        await api.post('/students', data);
        toast.success('Student created');
      }
      setModalOpen(false);
      fetchStudents();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const pages = Math.ceil(total / PAGE_SIZE);

  return (
    <>
      <Header title="Students" subtitle="Manage student records and profiles" />
      <main className="flex-1 p-6">
        <Card padding={false}>
          {/* Toolbar */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 border-b border-gray-200">
            <div className="relative w-full sm:w-72">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                className="pl-9 pr-3 py-2 w-full text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Search by name or admission no…"
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              />
            </div>
            <Button onClick={openCreate}>
              <PlusIcon className="h-4 w-4" /> Add Student
            </Button>
          </div>

          {/* Table */}
          <Table>
            <Thead>
              <tr>
                <Th>Admission No.</Th>
                <Th>Name</Th>
                <Th>Class</Th>
                <Th>Gender</Th>
                <Th>Phone</Th>
                <Th>Status</Th>
                <Th>Actions</Th>
              </tr>
            </Thead>
            <Tbody>
              {loading ? (
                <tr><td colSpan={7} className="text-center py-8 text-gray-400 text-sm">Loading…</td></tr>
              ) : students.length === 0 ? (
                <EmptyRow colSpan={7} />
              ) : (
                students.map((s) => (
                  <Tr key={s.id}>
                    <Td className="font-mono text-xs">{s.admission_number}</Td>
                    <Td className="font-medium">{s.full_name}</Td>
                    <Td>{s.class_name ? `${s.class_name}${s.section_name ? ` – ${s.section_name}` : ''}` : '—'}</Td>
                    <Td>{s.gender}</Td>
                    <Td>{s.phone || '—'}</Td>
                    <Td>
                      <Badge variant={s.is_active ? 'success' : 'neutral'}>
                        {s.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </Td>
                    <Td>
                      <button onClick={() => openEdit(s)} className="text-primary-600 hover:text-primary-800">
                        <PencilIcon className="h-4 w-4" />
                      </button>
                    </Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>

          {!loading && total > 0 && (
            <Pagination page={page} pages={pages} total={total} size={PAGE_SIZE} onPage={setPage} />
          )}
        </Card>
      </main>

      {/* Create / Edit Modal */}
      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Student' : 'Add Student'} size="lg">
        <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input
            label="Admission Number"
            error={errors.admission_number?.message}
            {...register('admission_number', { required: 'Required' })}
          />
          <Input
            label="Full Name"
            error={errors.full_name?.message}
            {...register('full_name', { required: 'Required' })}
          />
          <Input
            label="Date of Birth"
            type="date"
            error={errors.date_of_birth?.message}
            {...register('date_of_birth', { required: 'Required' })}
          />
          <Select
            label="Gender"
            options={[
              { value: 'Male',   label: 'Male' },
              { value: 'Female', label: 'Female' },
              { value: 'Other',  label: 'Other' },
            ]}
            placeholder="Select gender"
            error={errors.gender?.message}
            {...register('gender', { required: 'Required' })}
          />
          <Input label="Phone" type="tel" {...register('phone')} />
          <Input label="Email" type="email" {...register('email')} />
          <Input label="Address" className="sm:col-span-2" {...register('address', { required: 'Required' })} error={errors.address?.message} />

          <div className="sm:col-span-2 flex justify-end gap-3 pt-2">
            <Button variant="secondary" type="button" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button type="submit" loading={saving}>{editing ? 'Save Changes' : 'Create Student'}</Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
