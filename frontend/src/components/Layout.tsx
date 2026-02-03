import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  Home, 
  UserPlus, 
  CheckSquare, 
  Users, 
  Settings, 
  Folder,
  Activity
} from 'lucide-react'
import { useWebSocket } from '../lib/websocket'
import { useAppStore } from '../lib/store'
import { cn } from '../lib/utils'

interface LayoutProps {
  children: ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Onboard Client', href: '/onboard', icon: UserPlus },
  { name: 'Tasks', href: '/tasks', icon: CheckSquare },
  { name: 'Agents', href: '/agents', icon: Users },
  { name: 'Configuration', href: '/config', icon: Settings },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const { wsConnected } = useAppStore()
  
  // Initialize WebSocket connection
  useWebSocket()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="fixed inset-y-0 left-0 w-64 bg-gray-900">
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center gap-2 px-6 bg-gray-800">
            <Folder className="h-8 w-8 text-primary-400" />
            <div>
              <h1 className="text-lg font-bold text-white">SEO-SWARM</h1>
              <div className="flex items-center gap-2">
                <Activity className={cn(
                  "h-3 w-3",
                  wsConnected ? "text-green-400" : "text-gray-500"
                )} />
                <span className="text-xs text-gray-400">
                  {wsConnected ? 'Live' : 'Offline'}
                </span>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-gray-800 text-white'
                      : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                  )}
                >
                  <item.icon className="h-5 w-5" />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 text-xs text-gray-400">
            <p>v1.0.0</p>
            <p className="mt-1">Agent Swarm Dashboard</p>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="pl-64">
        <main className="py-8">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
