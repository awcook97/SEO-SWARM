import { create } from 'zustand'

interface WebSocketMessage {
  type: string
  [key: string]: any
}

interface AppState {
  wsConnected: boolean
  setWsConnected: (connected: boolean) => void
  notifications: WebSocketMessage[]
  addNotification: (notification: WebSocketMessage) => void
  clearNotifications: () => void
}

export const useAppStore = create<AppState>((set) => ({
  wsConnected: false,
  setWsConnected: (connected) => set({ wsConnected: connected }),
  notifications: [],
  addNotification: (notification) =>
    set((state) => ({
      notifications: [...state.notifications, notification],
    })),
  clearNotifications: () => set({ notifications: [] }),
}))
