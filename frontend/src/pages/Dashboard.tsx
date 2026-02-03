import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { 
  Users, 
  CheckSquare, 
  Folder, 
  TrendingUp,
  ArrowRight 
} from 'lucide-react'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import Button from '../components/Button'
import { listAgents, listTasks, listClients } from '../lib/api'
import { getStatusColor } from '../lib/utils'

export default function Dashboard() {
  const { data: agentsData, isLoading: agentsLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: () => listAgents().then(res => res.data),
  })

  const { data: tasksData, isLoading: tasksLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => listTasks().then(res => res.data),
  })

  const { data: clientsData, isLoading: clientsLoading } = useQuery({
    queryKey: ['clients'],
    queryFn: () => listClients().then(res => res.data),
  })

  const stats = [
    {
      name: 'Active Tasks',
      value: tasksData?.tasks?.filter((t: any) => t.status === 'DOING').length || 0,
      total: tasksData?.tasks?.length || 0,
      icon: CheckSquare,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      link: '/tasks',
    },
    {
      name: 'Agents',
      value: agentsData?.agents?.length || 0,
      total: agentsData?.agents?.length || 0,
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      link: '/agents',
    },
    {
      name: 'Clients',
      value: clientsData?.clients?.length || 0,
      total: clientsData?.clients?.length || 0,
      icon: Folder,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      link: '/onboard',
    },
  ]

  const recentTasks = tasksData?.tasks?.slice(0, 5) || []

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Manage your SEO agent swarm workflow
          </p>
        </div>
        <Link to="/onboard">
          <Button>
            <Users className="mr-2 h-4 w-4" />
            Onboard Client
          </Button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map((stat) => (
          <Link key={stat.name} to={stat.link}>
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">
                    {stat.value}
                    {stat.total !== stat.value && (
                      <span className="text-lg text-gray-500">/{stat.total}</span>
                    )}
                  </p>
                </div>
                <div className={`rounded-full p-3 ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>

      {/* Recent Tasks */}
      <Card
        title="Recent Tasks"
        description="Latest task activity"
        action={
          <Link to="/tasks">
            <Button variant="ghost" size="sm">
              View All <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        }
      >
        {tasksLoading ? (
          <LoadingSpinner />
        ) : recentTasks.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No tasks found. Create your first task!
          </div>
        ) : (
          <div className="space-y-3">
            {recentTasks.map((task: any) => (
              <div
                key={task.id}
                className="flex items-center justify-between rounded-lg border border-gray-200 p-4 hover:bg-gray-50"
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`h-3 w-3 rounded-full ${getStatusColor(task.status)}`}
                  />
                  <div>
                    <p className="font-medium text-gray-900">{task.title}</p>
                    <p className="text-sm text-gray-500">
                      {task.owner} • {task.priority}
                    </p>
                  </div>
                </div>
                <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700">
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Quick Actions */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card title="Quick Actions">
          <div className="space-y-3">
            <Link to="/onboard">
              <Button variant="ghost" className="w-full justify-start">
                <Users className="mr-2 h-4 w-4" />
                Onboard New Client
              </Button>
            </Link>
            <Link to="/tasks">
              <Button variant="ghost" className="w-full justify-start">
                <CheckSquare className="mr-2 h-4 w-4" />
                Create Task
              </Button>
            </Link>
            <Link to="/agents">
              <Button variant="ghost" className="w-full justify-start">
                <TrendingUp className="mr-2 h-4 w-4" />
                View Agents
              </Button>
            </Link>
          </div>
        </Card>

        <Card title="System Status">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Agents Available</span>
              <span className="font-medium text-gray-900">
                {agentsData?.agents?.length || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Active Clients</span>
              <span className="font-medium text-gray-900">
                {clientsData?.clients?.length || 0}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Pending Tasks</span>
              <span className="font-medium text-gray-900">
                {tasksData?.tasks?.filter((t: any) => t.status === 'TODO').length || 0}
              </span>
            </div>
          </div>
        </Card>

        <Card title="Recent Clients">
          {clientsLoading ? (
            <LoadingSpinner size="sm" />
          ) : clientsData?.clients?.length === 0 ? (
            <p className="text-sm text-gray-500">No clients yet</p>
          ) : (
            <div className="space-y-2">
              {clientsData?.clients?.slice(0, 5).map((client: any) => (
                <Link
                  key={client.slug}
                  to={`/clients/${client.slug}`}
                  className="block rounded p-2 hover:bg-gray-50"
                >
                  <p className="text-sm font-medium text-gray-900">{client.slug}</p>
                  <p className="text-xs text-gray-500">
                    {client.has_inputs ? '✓ Inputs ready' : '○ Pending setup'}
                  </p>
                </Link>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}
