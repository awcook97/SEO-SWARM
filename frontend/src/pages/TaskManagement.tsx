import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import Card from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import LoadingSpinner from '../components/LoadingSpinner'
import { listTasks, createTask, updateTask, startTask, Task } from '../lib/api'
import { getStatusColor, getPriorityColor, formatDate } from '../lib/utils'
import { Plus, Filter, Search } from 'lucide-react'

export default function TaskManagement() {
  const queryClient = useQueryClient()
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [filter, setFilter] = useState<string>('all')
  const [search, setSearch] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'med',
    owner: 'ORCHESTRATOR',
  })

  const { data: tasksData, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => listTasks().then(res => res.data),
    refetchInterval: 10000, // Refetch every 10 seconds
  })

  const createMutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      toast.success('Task created successfully')
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setShowCreateForm(false)
      setFormData({ title: '', description: '', priority: 'med', owner: 'ORCHESTRATOR' })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create task')
    },
  })

  const startMutation = useMutation({
    mutationFn: startTask,
    onSuccess: () => {
      toast.success('Task started')
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to start task')
    },
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.title || !formData.description) {
      toast.error('Title and description are required')
      return
    }
    createMutation.mutate(formData)
  }

  const tasks = tasksData?.tasks || []
  
  const filteredTasks = tasks.filter((task: Task) => {
    const matchesSearch = task.title.toLowerCase().includes(search.toLowerCase()) ||
                         task.description.toLowerCase().includes(search.toLowerCase())
    const matchesFilter = filter === 'all' || task.status === filter
    return matchesSearch && matchesFilter
  })

  const statusCounts = {
    all: tasks.length,
    TODO: tasks.filter((t: Task) => t.status === 'TODO').length,
    DOING: tasks.filter((t: Task) => t.status === 'DOING').length,
    DONE: tasks.filter((t: Task) => t.status === 'DONE').length,
    BLOCKED: tasks.filter((t: Task) => t.status === 'BLOCKED').length,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Task Management</h1>
          <p className="mt-2 text-gray-600">
            Create and track tasks across your agent swarm
          </p>
        </div>
        <Button onClick={() => setShowCreateForm(!showCreateForm)}>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </div>

      {/* Create Form */}
      {showCreateForm && (
        <Card>
          <form onSubmit={handleCreate} className="space-y-4">
            <Input
              label="Title"
              placeholder="Task title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
            
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                className="flex min-h-[100px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Task description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Priority
                </label>
                <select
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="med">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Owner
                </label>
                <select
                  className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  value={formData.owner}
                  onChange={(e) => setFormData({ ...formData, owner: e.target.value })}
                >
                  <option value="ORCHESTRATOR">ORCHESTRATOR</option>
                  <option value="PLANNER">PLANNER</option>
                  <option value="CODER">CODER</option>
                  <option value="TESTER">TESTER</option>
                  <option value="DOCS">DOCS</option>
                  <option value="REVIEWER">REVIEWER</option>
                  <option value="INTEGRATOR">INTEGRATOR</option>
                </select>
              </div>
            </div>

            <div className="flex gap-3">
              <Button type="submit" disabled={createMutation.isPending}>
                Create Task
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => setShowCreateForm(false)}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search tasks..."
              className="h-10 w-full rounded-md border border-gray-300 bg-white pl-10 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        
        <div className="flex gap-2">
          {Object.entries(statusCounts).map(([status, count]) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                filter === status
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {status} ({count})
            </button>
          ))}
        </div>
      </div>

      {/* Tasks List */}
      <Card>
        {isLoading ? (
          <LoadingSpinner />
        ) : filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No tasks found</p>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredTasks.map((task: Task) => (
              <div
                key={task.id}
                className="rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span
                        className={`h-3 w-3 rounded-full ${getStatusColor(task.status)}`}
                      />
                      <h3 className="font-semibold text-gray-900">{task.title}</h3>
                      <span className={`rounded-full px-2 py-1 text-xs font-medium ${getPriorityColor(task.priority)}`}>
                        {task.priority}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>ID: {task.id}</span>
                      <span>Owner: {task.owner}</span>
                      {task.created_at && <span>Created: {formatDate(task.created_at)}</span>}
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 text-center">
                      {task.status}
                    </span>
                    {task.status === 'TODO' && (
                      <Button
                        size="sm"
                        onClick={() => startMutation.mutate(task.id)}
                        disabled={startMutation.isPending}
                      >
                        Start
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
