import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ClientOnboarding from './pages/ClientOnboarding'
import TaskManagement from './pages/TaskManagement'
import AgentViewer from './pages/AgentViewer'
import ClientOutputs from './pages/ClientOutputs'
import Configuration from './pages/Configuration'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/onboard" element={<ClientOnboarding />} />
        <Route path="/tasks" element={<TaskManagement />} />
        <Route path="/agents" element={<AgentViewer />} />
        <Route path="/clients/:slug" element={<ClientOutputs />} />
        <Route path="/config" element={<Configuration />} />
      </Routes>
    </Layout>
  )
}

export default App
