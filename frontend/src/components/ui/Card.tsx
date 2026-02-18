import { HTMLAttributes } from 'react';
import clsx from 'clsx';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: boolean;
}

export function Card({ children, className, padding = true, ...props }: CardProps) {
  return (
    <div
      className={clsx('bg-white rounded-xl shadow-sm border border-gray-200', padding && 'p-6', className)}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={clsx('flex items-center justify-between mb-4', className)} {...props}>
      {children}
    </div>
  );
}

export function CardTitle({ children, className, ...props }: HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3 className={clsx('text-lg font-semibold text-gray-900', className)} {...props}>
      {children}
    </h3>
  );
}

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: { value: number; label: string };
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple';
}

const colorMap = {
  blue:   { bg: 'bg-blue-50',   icon: 'bg-blue-500',   text: 'text-blue-600' },
  green:  { bg: 'bg-green-50',  icon: 'bg-green-500',  text: 'text-green-600' },
  yellow: { bg: 'bg-yellow-50', icon: 'bg-yellow-500', text: 'text-yellow-600' },
  red:    { bg: 'bg-red-50',    icon: 'bg-red-500',    text: 'text-red-600' },
  purple: { bg: 'bg-purple-50', icon: 'bg-purple-500', text: 'text-purple-600' },
};

export function StatCard({ title, value, icon, trend, color = 'blue' }: StatCardProps) {
  const c = colorMap[color];
  return (
    <div className={clsx('rounded-xl p-6 flex items-start justify-between', c.bg)}>
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
        {trend && (
          <p className={clsx('text-xs mt-1', trend.value >= 0 ? 'text-green-600' : 'text-red-600')}>
            {trend.value >= 0 ? '▲' : '▼'} {Math.abs(trend.value)}% {trend.label}
          </p>
        )}
      </div>
      <div className={clsx('rounded-lg p-3 text-white', c.icon)}>{icon}</div>
    </div>
  );
}
