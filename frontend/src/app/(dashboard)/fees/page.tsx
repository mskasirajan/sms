'use client';

import { useEffect, useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { MagnifyingGlassIcon, CurrencyRupeeIcon } from '@heroicons/react/24/outline';
import { Header } from '@/components/layout/Header';
import { Card, StatCard } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Input';
import { feeStatusBadge } from '@/components/ui/Badge';
import { Table, Thead, Tbody, Th, Td, Tr, EmptyRow, Pagination } from '@/components/ui/Table';
import { Modal } from '@/components/ui/Modal';
import { api, getErrorMessage } from '@/lib/api';
import type { Invoice, Payment, PaymentCreate, PaginatedResponse } from '@/types';

export default function FeesPage() {
  const [invoices, setInvoices]   = useState<Invoice[]>([]);
  const [total, setTotal]         = useState(0);
  const [page, setPage]           = useState(1);
  const [search, setSearch]       = useState('');
  const [statusFilter, setStatus] = useState('');
  const [loading, setLoading]     = useState(false);
  const [payModal, setPayModal]   = useState<Invoice | null>(null);
  const [paying, setPaying]       = useState(false);

  const PAGE_SIZE = 10;
  const { register, handleSubmit, reset, formState: { errors } } = useForm<PaymentCreate>();

  const stats = {
    totalDue:       invoices.reduce((s, i) => s + i.due_amount, 0),
    totalCollected: invoices.reduce((s, i) => s + i.paid_amount, 0),
    overdue:        invoices.filter((i) => i.status === 'Overdue').length,
  };

  const fetchInvoices = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get<PaginatedResponse<Invoice>>('/fees/invoices', {
        params: { page, size: PAGE_SIZE, search: search || undefined, status: statusFilter || undefined },
      });
      setInvoices(data.items);
      setTotal(data.total);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => { fetchInvoices(); }, [fetchInvoices]);

  const openPayment = (inv: Invoice) => {
    setPayModal(inv);
    reset({ invoice_id: inv.id, payment_method: 'Cash' });
  };

  const submitPayment = async (data: PaymentCreate) => {
    setPaying(true);
    try {
      await api.post<Payment>('/fees/payment', { ...data, invoice_id: payModal!.id });
      toast.success('Payment recorded');
      setPayModal(null);
      fetchInvoices();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setPaying(false);
    }
  };

  const pages = Math.ceil(total / PAGE_SIZE);
  const fmt   = (n: number) => `₹${n.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;

  return (
    <>
      <Header title="Fees & Billing" subtitle="Track invoices and record payments" />
      <main className="flex-1 p-6 space-y-6">

        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard title="Total Collected" value={fmt(stats.totalCollected)} icon={<CurrencyRupeeIcon className="h-6 w-6" />} color="green" />
          <StatCard title="Outstanding Dues" value={fmt(stats.totalDue)}       icon={<CurrencyRupeeIcon className="h-6 w-6" />} color="yellow" />
          <StatCard title="Overdue Invoices" value={stats.overdue}             icon={<CurrencyRupeeIcon className="h-6 w-6" />} color="red" />
        </div>

        {/* Table */}
        <Card padding={false}>
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 p-4 border-b border-gray-200">
            <div className="relative w-full sm:w-72">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                className="pl-9 pr-3 py-2 w-full text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Search student name or admission no…"
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              />
            </div>
            <Select
              options={[
                { value: 'Pending', label: 'Pending' },
                { value: 'Partial', label: 'Partial' },
                { value: 'Paid',    label: 'Paid' },
                { value: 'Overdue', label: 'Overdue' },
              ]}
              placeholder="All statuses"
              value={statusFilter}
              onChange={(e) => { setStatus(e.target.value); setPage(1); }}
              className="w-44"
            />
          </div>

          <Table>
            <Thead>
              <tr>
                <Th>Student</Th>
                <Th>Admission No.</Th>
                <Th>Total</Th>
                <Th>Paid</Th>
                <Th>Due</Th>
                <Th>Due Date</Th>
                <Th>Status</Th>
                <Th>Action</Th>
              </tr>
            </Thead>
            <Tbody>
              {loading ? (
                <tr><td colSpan={8} className="text-center py-8 text-gray-400 text-sm">Loading…</td></tr>
              ) : invoices.length === 0 ? (
                <EmptyRow colSpan={8} />
              ) : (
                invoices.map((inv) => (
                  <Tr key={inv.id}>
                    <Td className="font-medium">{inv.student_name}</Td>
                    <Td className="font-mono text-xs">{inv.admission_number}</Td>
                    <Td>{fmt(inv.total_amount)}</Td>
                    <Td className="text-green-600">{fmt(inv.paid_amount)}</Td>
                    <Td className="text-red-600">{fmt(inv.due_amount)}</Td>
                    <Td>{inv.due_date}</Td>
                    <Td>{feeStatusBadge(inv.status)}</Td>
                    <Td>
                      {inv.status !== 'Paid' && (
                        <Button size="sm" onClick={() => openPayment(inv)}>Pay</Button>
                      )}
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

      {/* Payment Modal */}
      <Modal
        open={!!payModal}
        onClose={() => setPayModal(null)}
        title={`Record Payment — ${payModal?.student_name}`}
      >
        {payModal && (
          <form onSubmit={handleSubmit(submitPayment)} className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-3 text-sm space-y-1">
              <div className="flex justify-between"><span className="text-gray-500">Total Amount</span><span>{fmt(payModal.total_amount)}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Already Paid</span><span className="text-green-600">{fmt(payModal.paid_amount)}</span></div>
              <div className="flex justify-between font-semibold"><span>Balance Due</span><span className="text-red-600">{fmt(payModal.due_amount)}</span></div>
            </div>
            <Input
              label="Amount"
              type="number"
              step="0.01"
              max={payModal.due_amount}
              error={errors.amount?.message}
              {...register('amount', {
                required: 'Required',
                min: { value: 1, message: 'Must be > 0' },
                max: { value: payModal.due_amount, message: 'Cannot exceed due amount' },
              })}
            />
            <Select
              label="Payment Method"
              options={[
                { value: 'Cash',          label: 'Cash' },
                { value: 'UPI',           label: 'UPI' },
                { value: 'Card',          label: 'Card' },
                { value: 'Bank Transfer', label: 'Bank Transfer' },
              ]}
              error={errors.payment_method?.message}
              {...register('payment_method', { required: 'Required' })}
            />
            <Input label="Transaction ID (optional)" {...register('transaction_id')} />
            <div className="flex justify-end gap-3 pt-2">
              <Button variant="secondary" type="button" onClick={() => setPayModal(null)}>Cancel</Button>
              <Button type="submit" loading={paying}>Record Payment</Button>
            </div>
          </form>
        )}
      </Modal>
    </>
  );
}
