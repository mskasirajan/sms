'use client';

import { useEffect, useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { PlusIcon, MagnifyingGlassIcon, PencilIcon } from '@heroicons/react/24/outline';
import { Header } from '@/components/layout/Header';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { Table, Thead, Tbody, Th, Td, Tr, EmptyRow, Pagination } from '@/components/ui/Table';
import { Modal } from '@/components/ui/Modal';
import { api, getErrorMessage } from '@/lib/api';
import type { Teacher, TeacherCreate, PaginatedResponse } from '@/types';

export default function TeachersPage() {
  const [teachers, setTeachers]   = useState<Teacher[]>([]);
  const [total, setTotal]         = useState(0);
  const [page, setPage]           = useState(1);
  const [search, setSearch]       = useState('');
  const [loading, setLoading]     = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing]     = useState<Teacher | null>(null);
  const [saving, setSaving]       = useState(false);

  const PAGE_SIZE = 10;
  const { register, handleSubmit, reset, formState: { errors } } = useForm<TeacherCreate>();

  const fetchTeachers = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<PaginatedResponse<Teacher>>('/teachers', {
        params: { page, size: PAGE_SIZE, search: search || undefined },
      });
      setTeachers(data.items);
      setTotal(data.total);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchTeachers(); }, [fetchTeachers]);

  const openCreate = () => { setEditing(null); reset({}); setModalOpen(true); };
  const openEdit   = (t: Teacher) => {
    setEditing(t);
    reset({
      employee_id: t.employee_id, full_name: t.full_name, email: t.email,
      phone: t.phone, qualification: t.qualification,
      specialization: t.specialization, joining_date: t.joining_date,
    });
    setModalOpen(true);
  };

  const onSubmit = async (data: TeacherCreate) => {
    setSaving(true);
    try {
      if (editing) {
        await api.put(`/teachers/${editing.id}`, data);
        toast.success('Teacher updated');
      } else {
        await api.post('/teachers', data);
        toast.success('Teacher created');
      }
      setModalOpen(false);
      fetchTeachers();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const pages = Math.ceil(total / PAGE_SIZE);

  return (
    <>
      <Header title="Teachers" subtitle="Manage staff and teacher profiles" />
      <main className="flex-1 p-6">
        <Card padding={false}>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 border-b border-gray-200">
            <div className="relative w-full sm:w-72">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                className="pl-9 pr-3 py-2 w-full text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Search by name or employee ID…"
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              />
            </div>
            <Button onClick={openCreate}>
              <PlusIcon className="h-4 w-4" /> Add Teacher
            </Button>
          </div>

          <Table>
            <Thead>
              <tr>
                <Th>Employee ID</Th>
                <Th>Name</Th>
                <Th>Email</Th>
                <Th>Qualification</Th>
                <Th>Specialization</Th>
                <Th>Status</Th>
                <Th>Actions</Th>
              </tr>
            </Thead>
            <Tbody>
              {loading ? (
                <tr><td colSpan={7} className="text-center py-8 text-gray-400 text-sm">Loading…</td></tr>
              ) : teachers.length === 0 ? (
                <EmptyRow colSpan={7} />
              ) : (
                teachers.map((t) => (
                  <Tr key={t.id}>
                    <Td className="font-mono text-xs">{t.employee_id}</Td>
                    <Td className="font-medium">{t.full_name}</Td>
                    <Td>{t.email}</Td>
                    <Td>{t.qualification}</Td>
                    <Td>{t.specialization || '—'}</Td>
                    <Td>
                      <Badge variant={t.is_active ? 'success' : 'neutral'}>
                        {t.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </Td>
                    <Td>
                      <button onClick={() => openEdit(t)} className="text-primary-600 hover:text-primary-800">
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

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Edit Teacher' : 'Add Teacher'} size="lg">
        <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input label="Employee ID" error={errors.employee_id?.message} {...register('employee_id', { required: 'Required' })} />
          <Input label="Full Name"   error={errors.full_name?.message}   {...register('full_name',   { required: 'Required' })} />
          <Input label="Email" type="email" error={errors.email?.message} {...register('email', { required: 'Required' })} />
          <Input label="Phone" type="tel" error={errors.phone?.message}  {...register('phone', { required: 'Required' })} />
          <Input label="Qualification"  error={errors.qualification?.message} {...register('qualification', { required: 'Required' })} />
          <Input label="Specialization" {...register('specialization')} />
          <Input label="Joining Date" type="date" error={errors.joining_date?.message} {...register('joining_date', { required: 'Required' })} />

          <div className="sm:col-span-2 flex justify-end gap-3 pt-2">
            <Button variant="secondary" type="button" onClick={() => setModalOpen(false)}>Cancel</Button>
            <Button type="submit" loading={saving}>{editing ? 'Save Changes' : 'Create Teacher'}</Button>
          </div>
        </form>
      </Modal>
    </>
  );
}
