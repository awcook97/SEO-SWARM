import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import toast from 'react-hot-toast'
import Card from '../components/Card'
import Button from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'
import { getConfig, updateConfig, Config } from '../lib/api'
import { Settings, Save } from 'lucide-react'

export default function Configuration() {
  const queryClient = useQueryClient()
  const [editMode, setEditMode] = useState(false)
  const [editedConfig, setEditedConfig] = useState<Config | null>(null)

  const { data: configData, isLoading } = useQuery({
    queryKey: ['config'],
    queryFn: () => getConfig().then(res => res.data),
  })

  const updateMutation = useMutation({
    mutationFn: ({ key, value, isJson }: { key: string; value: any; isJson: boolean }) =>
      updateConfig(key, value, isJson),
    onSuccess: () => {
      toast.success('Configuration updated')
      queryClient.invalidateQueries({ queryKey: ['config'] })
      setEditMode(false)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update configuration')
    },
  })

  const config = configData?.config || {}

  const handleEdit = () => {
    setEditedConfig({ ...config })
    setEditMode(true)
  }

  const handleCancel = () => {
    setEditedConfig(null)
    setEditMode(false)
  }

  const handleSave = (key: string, value: any) => {
    const isJson = typeof value === 'object'
    updateMutation.mutate({ key, value, isJson })
  }

  const configSections = [
    {
      title: 'Workflow Settings',
      keys: ['workflow_mode', 'status_commit_policy', 'finish_auto_status_commit'],
    },
    {
      title: 'Branch Settings',
      keys: ['base_branch', 'branch.task_prefix'],
    },
    {
      title: 'Paths',
      keys: Object.keys(config.paths || {}).map(k => `paths.${k}`),
    },
  ]

  const getNestedValue = (obj: any, path: string) => {
    return path.split('.').reduce((acc, part) => acc?.[part], obj)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Configuration</h1>
          <p className="mt-2 text-gray-600">
            Manage swarm workflow and system settings
          </p>
        </div>
        {!editMode && (
          <Button onClick={handleEdit}>
            <Settings className="mr-2 h-4 w-4" />
            Edit Config
          </Button>
        )}
      </div>

      {isLoading ? (
        <Card>
          <LoadingSpinner />
        </Card>
      ) : (
        <div className="space-y-6">
          {configSections.map((section) => (
            <Card key={section.title} title={section.title}>
              <div className="space-y-4">
                {section.keys.map((key) => {
                  const value = getNestedValue(config, key)
                  const displayValue = typeof value === 'object'
                    ? JSON.stringify(value, null, 2)
                    : String(value)

                  return (
                    <div key={key} className="flex items-start justify-between border-b border-gray-100 pb-4 last:border-0 last:pb-0">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{key}</p>
                        {editMode ? (
                          <input
                            type="text"
                            className="mt-2 w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                            value={editedConfig ? getNestedValue(editedConfig, key) : displayValue}
                            onChange={(e) => {
                              if (editedConfig) {
                                const keys = key.split('.')
                                const newConfig = { ...editedConfig }
                                let current: any = newConfig
                                for (let i = 0; i < keys.length - 1; i++) {
                                  current = current[keys[i]]
                                }
                                current[keys[keys.length - 1]] = e.target.value
                                setEditedConfig(newConfig)
                              }
                            }}
                          />
                        ) : (
                          <p className="mt-1 font-mono text-sm text-gray-600">
                            {displayValue}
                          </p>
                        )}
                      </div>
                      {editMode && (
                        <Button
                          size="sm"
                          onClick={() => handleSave(key, getNestedValue(editedConfig, key))}
                          disabled={updateMutation.isPending}
                          className="ml-4"
                        >
                          <Save className="h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  )
                })}
              </div>
            </Card>
          ))}

          {editMode && (
            <div className="flex gap-3">
              <Button onClick={handleCancel} variant="secondary">
                Cancel
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Info */}
      <Card title="Configuration Help">
        <ul className="space-y-2 text-sm text-gray-600">
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span><strong>workflow_mode:</strong> Controls workflow guardrails (direct, branch_pr)</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span><strong>base_branch:</strong> The default branch for operations</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span><strong>status_commit_policy:</strong> How status updates are handled (warn, auto, manual)</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-primary-600">•</span>
            <span>Changes are applied immediately and persisted to .codex-swarm/config.json</span>
          </li>
        </ul>
      </Card>
    </div>
  )
}
