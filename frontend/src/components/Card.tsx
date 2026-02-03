import { ReactNode } from 'react'
import { cn } from '../lib/utils'

interface CardProps {
  children: ReactNode
  className?: string
  title?: string
  description?: string
  action?: ReactNode
}

export default function Card({ children, className, title, description, action }: CardProps) {
  return (
    <div className={cn('rounded-lg border border-gray-200 bg-white shadow-sm', className)}>
      {(title || description || action) && (
        <div className="flex items-start justify-between border-b border-gray-200 px-6 py-4">
          <div>
            {title && <h3 className="text-lg font-semibold text-gray-900">{title}</h3>}
            {description && <p className="mt-1 text-sm text-gray-500">{description}</p>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  )
}
