import { useQuery } from '@tanstack/react-query'
import Card from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import { listAgents, Agent } from '../lib/api'
import { Users, FileCode, Info } from 'lucide-react'

export default function AgentViewer() {
  const { data: agentsData, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: () => listAgents().then(res => res.data),
  })

  const agents = agentsData?.agents || []

  const agentRoles = [
    {
      category: 'Planning & Orchestration',
      agents: ['ORCHESTRATOR', 'PLANNER', 'CREATOR'],
      color: 'bg-purple-100 text-purple-800 border-purple-200',
    },
    {
      category: 'Development',
      agents: ['CODER', 'TESTER', 'DOCS'],
      color: 'bg-blue-100 text-blue-800 border-blue-200',
    },
    {
      category: 'SEO & Content',
      agents: ['LOCAL_SEO_STRATEGIST', 'COPYWRITER_SEO', 'CONTENT_PLANNER_SEO', 'ON_PAGE_SEO_SPECIALIST'],
      color: 'bg-green-100 text-green-800 border-green-200',
    },
    {
      category: 'Analysis & Reporting',
      agents: ['TECHNICAL_SEO_AUDITOR', 'SERP_ANALYST', 'ANALYTICS_REPORTING'],
      color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    },
    {
      category: 'Management & Operations',
      agents: ['GBP_OPTIMIZER', 'CITATION_MANAGER', 'REVIEW_REPUTATION', 'LOCAL_LINK_BUILDER'],
      color: 'bg-pink-100 text-pink-800 border-pink-200',
    },
    {
      category: 'Quality & Integration',
      agents: ['REVIEWER', 'INTEGRATOR', 'COMPLIANCE_EDITOR', 'UPDATER'],
      color: 'bg-indigo-100 text-indigo-800 border-indigo-200',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Agent Registry</h1>
        <p className="mt-2 text-gray-600">
          View all available agents in the swarm ecosystem
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-6 sm:grid-cols-3">
        <Card>
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-primary-100 p-3">
              <Users className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Agents</p>
              <p className="text-2xl font-bold text-gray-900">{agents.length}</p>
            </div>
          </div>
        </Card>
        
        <Card>
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-green-100 p-3">
              <FileCode className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Categories</p>
              <p className="text-2xl font-bold text-gray-900">{agentRoles.length}</p>
            </div>
          </div>
        </Card>
        
        <Card>
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-blue-100 p-3">
              <Info className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <p className="text-2xl font-bold text-green-600">Active</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Agents by Category */}
      {isLoading ? (
        <Card>
          <LoadingSpinner />
        </Card>
      ) : (
        <div className="space-y-6">
          {agentRoles.map((roleGroup) => {
            const categoryAgents = agents.filter((agent: Agent) =>
              roleGroup.agents.includes(agent.name)
            )

            if (categoryAgents.length === 0) return null

            return (
              <Card key={roleGroup.category} title={roleGroup.category}>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {categoryAgents.map((agent: Agent) => (
                    <div
                      key={agent.name}
                      className={`rounded-lg border p-4 ${roleGroup.color}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold">{agent.name}</h3>
                          {agent.description && (
                            <p className="mt-2 text-sm opacity-80">
                              {agent.description}
                            </p>
                          )}
                          {agent.role && (
                            <p className="mt-2 text-xs font-medium">
                              Role: {agent.role}
                            </p>
                          )}
                        </div>
                        <FileCode className="h-5 w-5 opacity-60" />
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            )
          })}

          {/* Other Agents */}
          {agents.filter((agent: Agent) => 
            !agentRoles.some(role => role.agents.includes(agent.name))
          ).length > 0 && (
            <Card title="Other Agents">
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {agents
                  .filter((agent: Agent) => 
                    !agentRoles.some(role => role.agents.includes(agent.name))
                  )
                  .map((agent: Agent) => (
                    <div
                      key={agent.name}
                      className="rounded-lg border border-gray-200 p-4 bg-gray-50"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{agent.name}</h3>
                          {agent.description && (
                            <p className="mt-2 text-sm text-gray-600">
                              {agent.description}
                            </p>
                          )}
                        </div>
                        <FileCode className="h-5 w-5 text-gray-400" />
                      </div>
                    </div>
                  ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
