import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | undefined): string {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getStatusColor(status: string): string {
  const statusColors: Record<string, string> = {
    TODO: 'bg-gray-500',
    DOING: 'bg-blue-500',
    BLOCKED: 'bg-red-500',
    DONE: 'bg-green-500',
    REVIEW: 'bg-yellow-500',
  }
  return statusColors[status] || 'bg-gray-500'
}

export function getPriorityColor(priority: string): string {
  const priorityColors: Record<string, string> = {
    low: 'bg-blue-100 text-blue-800',
    med: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800',
  }
  return priorityColors[priority] || 'bg-gray-100 text-gray-800'
}
