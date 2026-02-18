import clsx from 'clsx';

type BadgeVariant = 'success' | 'warning' | 'danger' | 'info' | 'neutral';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

const variants: Record<BadgeVariant, string> = {
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger:  'bg-red-100 text-red-800',
  info:    'bg-blue-100 text-blue-800',
  neutral: 'bg-gray-100 text-gray-800',
};

export function Badge({ children, variant = 'neutral', className }: BadgeProps) {
  return (
    <span className={clsx('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', variants[variant], className)}>
      {children}
    </span>
  );
}

// Convenience helpers
export function attendanceBadge(status: string) {
  const map: Record<string, BadgeVariant> = {
    Present:  'success',
    Absent:   'danger',
    Late:     'warning',
    'Half-Day': 'info',
  };
  return <Badge variant={map[status] || 'neutral'}>{status}</Badge>;
}

export function feeStatusBadge(status: string) {
  const map: Record<string, BadgeVariant> = {
    Paid:    'success',
    Pending: 'warning',
    Partial: 'info',
    Overdue: 'danger',
  };
  return <Badge variant={map[status] || 'neutral'}>{status}</Badge>;
}
