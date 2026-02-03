import { useEffect, useRef } from 'react'
import { useAppStore } from './store'
import toast from 'react-hot-toast'

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null)
  const { setWsConnected, addNotification } = useAppStore()

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws`)

    ws.onopen = () => {
      console.log('WebSocket connected')
      setWsConnected(true)
      toast.success('Connected to live updates')
    }

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        addNotification(message)

        // Show toast notifications for certain events
        if (message.type === 'task_created') {
          toast.success('New task created')
        } else if (message.type === 'task_updated') {
          toast.success(`Task ${message.task_id} updated`)
        } else if (message.type === 'client_onboarded') {
          toast.success(`Client ${message.slug} onboarded successfully`)
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      toast.error('WebSocket connection error')
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setWsConnected(false)
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [setWsConnected, addNotification])

  return wsRef.current
}
