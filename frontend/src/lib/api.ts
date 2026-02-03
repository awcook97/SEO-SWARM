import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Types
export interface Agent {
  name: string
  file: string
  role?: string
  description?: string
}

export interface Task {
  id: string
  title: string
  description: string
  status: string
  priority: string
  owner: string
  depends_on: string[]
  created_at?: string
  updated_at?: string
}

export interface Client {
  slug: string
  has_inputs: boolean
  path: string
}

export interface Config {
  workflow_mode: string
  base_branch: string
  [key: string]: any
}

// API functions
export const getHealth = () => api.get('/health')

export const getConfig = () => api.get<{ config: Config }>('/config')

export const updateConfig = (key: string, value: any, isJson = false) =>
  api.post('/config', { key, value, is_json: isJson })

export const listAgents = () => api.get<{ agents: Agent[] }>('/agents')

export const getAgent = (name: string) => api.get<{ agent: any }>(`/agents/${name}`)

export const listTasks = () => api.get<{ tasks: Task[] }>('/tasks')

export const getTask = (id: string) => api.get(`/tasks/${id}`)

export const createTask = (task: {
  title: string
  description: string
  priority?: string
  owner?: string
}) => api.post('/tasks', task)

export const updateTask = (
  id: string,
  task: {
    title?: string
    description?: string
    priority?: string
    owner?: string
  }
) => api.patch(`/tasks/${id}`, task)

export const startTask = (id: string) => api.post(`/tasks/${id}/start`)

export const finishTask = (id: string, commit: string, author = 'USER') =>
  api.post(`/tasks/${id}/finish`, null, { params: { commit, author } })

export const onboardClient = (client: {
  name: string
  slug: string
  website?: string
  crawl_site?: boolean
}) => api.post('/clients/onboard', client)

export const listClients = () => api.get<{ clients: Client[] }>('/clients')

export const getClientOutputs = (slug: string) =>
  api.get<{ slug: string; outputs: any }>(`/clients/${slug}/outputs`)
