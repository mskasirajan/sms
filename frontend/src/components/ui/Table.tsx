import { HTMLAttributes } from 'react';
import clsx from 'clsx';

export function Table({ children, className }: HTMLAttributes<HTMLTableElement>) {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className={clsx('min-w-full divide-y divide-gray-200 text-sm', className)}>
        {children}
      </table>
    </div>
  );
}

export function Thead({ children }: { children: React.ReactNode }) {
  return <thead className="bg-gray-50">{children}</thead>;
}

export function Tbody({ children }: { children: React.ReactNode }) {
  return <tbody className="bg-white divide-y divide-gray-100">{children}</tbody>;
}

export function Th({ children, className }: HTMLAttributes<HTMLTableCellElement>) {
  return (
    <th className={clsx('px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider', className)}>
      {children}
    </th>
  );
}

export function Td({ children, className }: HTMLAttributes<HTMLTableCellElement>) {
  return (
    <td className={clsx('px-4 py-3 text-gray-800 whitespace-nowrap', className)}>
      {children}
    </td>
  );
}

export function Tr({ children, className, onClick }: HTMLAttributes<HTMLTableRowElement>) {
  return (
    <tr
      className={clsx('hover:bg-gray-50 transition-colors', onClick && 'cursor-pointer', className)}
      onClick={onClick}
    >
      {children}
    </tr>
  );
}

// ─── Empty State ──────────────────────────────────────────────────────────────

export function EmptyRow({ colSpan, message = 'No records found' }: { colSpan: number; message?: string }) {
  return (
    <tr>
      <td colSpan={colSpan} className="text-center py-10 text-gray-400 text-sm">
        {message}
      </td>
    </tr>
  );
}

// ─── Pagination ───────────────────────────────────────────────────────────────

interface PaginationProps {
  page: number;
  pages: number;
  total: number;
  size: number;
  onPage: (p: number) => void;
}

export function Pagination({ page, pages, total, size, onPage }: PaginationProps) {
  const from = (page - 1) * size + 1;
  const to   = Math.min(page * size, total);
  return (
    <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 bg-white text-sm text-gray-600">
      <span>Showing {from}–{to} of {total}</span>
      <div className="flex gap-1">
        <button
          disabled={page <= 1}
          onClick={() => onPage(page - 1)}
          className="px-2 py-1 rounded border border-gray-300 disabled:opacity-40 hover:bg-gray-50"
        >
          ‹ Prev
        </button>
        {Array.from({ length: pages }, (_, i) => i + 1)
          .filter((p) => p === 1 || p === pages || Math.abs(p - page) <= 1)
          .map((p, idx, arr) => (
            <>
              {idx > 0 && arr[idx - 1] !== p - 1 && (
                <span key={`ellipsis-${p}`} className="px-2 py-1">…</span>
              )}
              <button
                key={p}
                onClick={() => onPage(p)}
                className={clsx(
                  'px-3 py-1 rounded border',
                  p === page ? 'bg-primary-600 text-white border-primary-600' : 'border-gray-300 hover:bg-gray-50'
                )}
              >
                {p}
              </button>
            </>
          ))}
        <button
          disabled={page >= pages}
          onClick={() => onPage(page + 1)}
          className="px-2 py-1 rounded border border-gray-300 disabled:opacity-40 hover:bg-gray-50"
        >
          Next ›
        </button>
      </div>
    </div>
  );
}
