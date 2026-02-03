import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import { getClientOutputs } from '../lib/api'
import { Folder, FileText, Download } from 'lucide-react'

export default function ClientOutputs() {
  const { slug } = useParams<{ slug: string }>()

  const { data, isLoading, error } = useQuery({
    queryKey: ['client-outputs', slug],
    queryFn: () => getClientOutputs(slug!).then(res => res.data),
    enabled: !!slug,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <Card>
        <div className="text-center py-8">
          <p className="text-red-600">Failed to load client outputs</p>
        </div>
      </Card>
    )
  }

  const outputs = data?.outputs || {}
  const categories = [
    { key: 'reports', label: 'Reports', icon: FileText, color: 'text-blue-600' },
    { key: 'pages', label: 'Pages', icon: FileText, color: 'text-green-600' },
    { key: 'articles', label: 'Articles', icon: FileText, color: 'text-purple-600' },
    { key: 'social', label: 'Social', icon: FileText, color: 'text-pink-600' },
    { key: 'email', label: 'Email', icon: FileText, color: 'text-yellow-600' },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <Folder className="h-8 w-8 text-primary-600" />
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Client: {slug}</h1>
          <p className="mt-1 text-gray-600">View all generated outputs and reports</p>
        </div>
      </div>

      {/* Output Categories */}
      <div className="grid gap-6 lg:grid-cols-2">
        {categories.map((category) => {
          const files = outputs[category.key] || []
          
          return (
            <Card
              key={category.key}
              title={category.label}
              description={`${files.length} file${files.length !== 1 ? 's' : ''}`}
            >
              {files.length === 0 ? (
                <p className="text-sm text-gray-500">No files in this category</p>
              ) : (
                <div className="space-y-2">
                  {files.map((file: any) => (
                    <div
                      key={file.path}
                      className="flex items-center justify-between rounded-lg border border-gray-200 p-3 hover:bg-gray-50"
                    >
                      <div className="flex items-center gap-3">
                        <category.icon className={`h-5 w-5 ${category.color}`} />
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {file.name}
                          </p>
                          <p className="text-xs text-gray-500">{file.path}</p>
                        </div>
                      </div>
                      <button
                        className="rounded p-1 hover:bg-gray-100"
                        title="View file"
                      >
                        <Download className="h-4 w-4 text-gray-600" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )
        })}
      </div>

      {/* Summary */}
      <Card title="Summary">
        <div className="grid gap-4 sm:grid-cols-5">
          {categories.map((category) => {
            const count = (outputs[category.key] || []).length
            return (
              <div key={category.key} className="text-center">
                <p className="text-2xl font-bold text-gray-900">{count}</p>
                <p className="text-sm text-gray-600">{category.label}</p>
              </div>
            )
          })}
        </div>
      </Card>
    </div>
  )
}
