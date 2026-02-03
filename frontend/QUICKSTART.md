# SEO-SWARM Frontend - Quick Start Guide

## 🚀 Installation & Setup

### Option 1: Automated Start (Recommended)

**Linux/Mac:**
```bash
cd frontend
./start.sh
```

**Windows:**
```cmd
cd frontend
start.bat
```

This script will:
- Check prerequisites (Python 3, Node.js)
- Set up Python virtual environment
- Install backend dependencies
- Start FastAPI backend server (port 8000)
- Install frontend dependencies
- Start Vite dev server (port 5173)

### Option 2: Manual Start

**Backend:**
```bash
cd frontend/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Frontend (in new terminal):**
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Access Points

Once running, access the dashboard at:

- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **WebSocket**: ws://localhost:8000/ws

## 📋 First Steps

### 1. Onboard Your First Client

1. Click **Onboard Client** in the sidebar
2. Fill in:
   - Client Name: "Demo HVAC Company"
   - Slug: "demo-hvac" (auto-generated)
   - Website: "https://example.com" (optional)
   - ☑ Crawl site (if you want to cache HTML)
3. Click **Onboard Client**

Result: Creates `data/outputs/demo-hvac/` with scaffolded files

### 2. Create a Task

1. Click **Tasks** in sidebar
2. Click **New Task**
3. Fill in:
   - Title: "Create homepage schema"
   - Description: "Generate JSON-LD schema for homepage"
   - Priority: Medium
   - Owner: LOCAL_SEO_STRATEGIST
4. Click **Create Task**

### 3. Monitor Progress

- Dashboard shows real-time stats
- Green "Live" indicator = WebSocket connected
- Toast notifications for events
- Task status updates automatically

## 🎯 Key Features

### Client Onboarding
- Automated workspace scaffolding
- Optional website crawling
- Pre-filled input templates
- Directory structure creation

### Task Management
- Create/update/track tasks
- Filter by status (TODO/DOING/DONE/BLOCKED)
- Search functionality
- Priority levels
- Agent assignment

### Agent Registry
- View all 20+ agents
- Organized by category:
  - Planning & Orchestration
  - Development
  - SEO & Content
  - Analysis & Reporting
  - Management & Operations
  - Quality & Integration

### Real-time Updates
- WebSocket connection
- Live task updates
- Toast notifications
- Auto-refresh data

### Configuration Management
- Edit workflow settings
- Modify branch configuration
- Update file paths
- Change workflow mode

## 🔧 Configuration

Edit settings in **Configuration** page or directly in `.codex-swarm/config.json`:

```json
{
  "workflow_mode": "direct",
  "status_commit_policy": "warn",
  "base_branch": "main",
  "paths": {
    "agents_dir": ".codex-swarm/agents",
    "tasks_path": ".codex-swarm/tasks.json",
    "workflow_dir": ".codex-swarm/tasks"
  }
}
```

## 📊 Dashboard Overview

### Stats Cards
- **Active Tasks**: Currently in-progress tasks
- **Agents**: Total available agents
- **Clients**: Onboarded clients

### Recent Tasks
- Last 5 tasks created
- Quick status view
- Direct links to details

### Quick Actions
- One-click navigation to key features
- System status monitoring
- Recent client list

## 🛠 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in backend/main.py
```

**Module not found:**
```bash
cd frontend/backend
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Change port in vite.config.ts
export default defineConfig({
  server: { port: 3000 }
})
```

**Dependencies error:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### WebSocket Connection Failed

1. Verify backend is running on port 8000
2. Check browser console for errors
3. Disable browser extensions that block WebSockets
4. Check firewall settings

## 📁 Project Structure

```
frontend/
├── backend/
│   ├── main.py                 # FastAPI server
│   └── requirements.txt        # Python deps
├── src/
│   ├── components/             # UI components
│   ├── pages/                  # Route pages
│   ├── lib/                    # Utils & API
│   └── main.tsx               # Entry point
├── start.sh                    # Unix start script
├── start.bat                   # Windows start script
└── README.md                   # Full documentation
```

## 🚢 Production Deployment

### Build for Production

```bash
cd frontend
npm run build
```

Outputs to `frontend/dist/` - FastAPI automatically serves these files.

### Docker Deployment

```bash
cd frontend
docker build -t seo-swarm-ui .
docker run -p 8000:8000 -v $(pwd)/../..:/workspace seo-swarm-ui
```

### Environment Variables

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 🔐 Security Notes

- Frontend is for local development use
- No authentication implemented (add if exposing publicly)
- WebSocket messages are unencrypted (use WSS in production)
- API accepts CORS from localhost only

## 💡 Tips & Best Practices

1. **Keep backend running**: Frontend needs API access
2. **Monitor WebSocket**: Green indicator = live updates
3. **Use search**: Filter tasks and clients quickly
4. **Check console**: Browser dev tools show detailed logs
5. **Refresh on errors**: F5 if UI gets out of sync

## 🆘 Getting Help

- Check `frontend/README.md` for detailed docs
- View API docs at http://localhost:8000/docs
- Review backend logs in terminal
- Check browser console for frontend errors

## 🎉 Next Steps

After setup:
1. Onboard a real client with actual data
2. Create tasks for SEO workflow
3. Explore agent capabilities
4. Generate reports and content
5. Configure workflow settings

Happy automating! 🚀
