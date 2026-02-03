# SEO-SWARM Frontend - First Run Checklist

Use this checklist to ensure everything is set up correctly for your first run.

## Prerequisites ✓

- [ ] **Python 3.10+** installed
  ```bash
  python3 --version  # Should show 3.10 or higher
  ```

- [ ] **Node.js 18+** installed
  ```bash
  node --version  # Should show v18 or higher
  npm --version   # Should be installed with Node
  ```

- [ ] **Git** installed (for the main project)
  ```bash
  git --version
  ```

## Installation Steps ✓

### Option A: Automated Setup (Recommended)

- [ ] Navigate to frontend directory
  ```bash
  cd /home/andrew/projects/codex-swarm/frontend
  ```

- [ ] Run the start script
  ```bash
  ./start.sh          # Linux/Mac
  # OR
  start.bat           # Windows
  ```

- [ ] Wait for both servers to start
  - Backend should show: "Uvicorn running on http://0.0.0.0:8000"
  - Frontend should show: "Local: http://localhost:5173"

### Option B: Manual Setup

#### Backend Setup
- [ ] Create Python virtual environment
  ```bash
  cd frontend/backend
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  source venv/bin/activate  # Linux/Mac
  # OR
  venv\Scripts\activate     # Windows
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Start backend server
  ```bash
  python main.py
  ```
  Should see: "Application startup complete"

#### Frontend Setup (New Terminal)
- [ ] Install Node dependencies
  ```bash
  cd frontend
  npm install
  ```
  Wait for installation to complete (~2-3 minutes first time)

- [ ] Start development server
  ```bash
  npm run dev
  ```
  Should see: "VITE ready in XXX ms"

## Verify Installation ✓

- [ ] **Backend Health Check**
  - Open http://localhost:8000/api/health
  - Should see: `{"status": "ok", "project_root": "..."}`

- [ ] **API Documentation**
  - Open http://localhost:8000/docs
  - Should see Swagger UI with API endpoints

- [ ] **Frontend Access**
  - Open http://localhost:5173
  - Should see SEO-SWARM Dashboard

- [ ] **WebSocket Connection**
  - Check sidebar in UI
  - Should show green "Live" indicator

## First Actions ✓

### 1. Test Client Onboarding
- [ ] Click "Onboard Client" in sidebar
- [ ] Fill in form:
  - Client Name: "Test HVAC Company"
  - Slug: "test-hvac"
  - Website: Leave empty for now
  - Crawl site: Unchecked
- [ ] Click "Onboard Client"
- [ ] Verify success:
  - Toast notification appears
  - Client appears in dashboard
  - Directory created: `data/outputs/test-hvac/`

### 2. Create a Test Task
- [ ] Click "Tasks" in sidebar
- [ ] Click "New Task" button
- [ ] Fill in form:
  - Title: "Setup homepage schema"
  - Description: "Create JSON-LD schema for homepage"
  - Priority: Medium
  - Owner: LOCAL_SEO_STRATEGIST
- [ ] Click "Create Task"
- [ ] Verify success:
  - Task appears in list
  - Toast notification
  - Status shows "TODO"

### 3. Browse Agents
- [ ] Click "Agents" in sidebar
- [ ] Verify agent categories load:
  - Planning & Orchestration
  - Development
  - SEO & Content
  - Analysis & Reporting
  - Management & Operations
  - Quality & Integration
- [ ] Count total agents (should be 20+)

### 4. Check Configuration
- [ ] Click "Configuration" in sidebar
- [ ] Verify settings load:
  - workflow_mode: "direct"
  - base_branch: "main"
  - Various paths shown
- [ ] No need to change anything yet

## Troubleshooting ✓

### Backend Issues

**Problem: Port 8000 already in use**
- [ ] Find and kill process:
  ```bash
  # Linux/Mac
  lsof -i :8000
  kill <PID>
  
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

**Problem: Module not found (Python)**
- [ ] Verify virtual environment is activated
- [ ] Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```

**Problem: Can't find agentctl.py**
- [ ] Verify you're in the correct directory
- [ ] Check path in backend/main.py (line 26):
  ```python
  AGENTCTL_PATH = PROJECT_ROOT / ".codex-swarm" / "agentctl.py"
  ```

### Frontend Issues

**Problem: Port 5173 already in use**
- [ ] Find and kill process or change port in vite.config.ts

**Problem: npm install fails**
- [ ] Clear cache and retry:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

**Problem: TypeScript errors**
- [ ] Ensure TypeScript is installed:
  ```bash
  npm install -D typescript
  ```

### WebSocket Issues

**Problem: "Offline" status in sidebar**
- [ ] Verify backend is running on port 8000
- [ ] Check browser console for errors
- [ ] Try refreshing the page (F5)
- [ ] Check firewall/antivirus settings

**Problem: No toast notifications**
- [ ] WebSocket might be disconnected
- [ ] Check browser console for WebSocket errors
- [ ] Restart both servers

## Performance Check ✓

- [ ] **Page Load Time**
  - Dashboard should load in < 2 seconds
  - Subsequent pages should load instantly

- [ ] **API Response Time**
  - Open browser DevTools → Network tab
  - API calls should complete in < 500ms

- [ ] **WebSocket Connection**
  - Should connect immediately on page load
  - Should auto-reconnect if dropped

- [ ] **Memory Usage**
  - Frontend: < 200MB RAM
  - Backend: < 100MB RAM

## Next Steps ✓

- [ ] Read [QUICKSTART.md](QUICKSTART.md) for detailed usage guide
- [ ] Review [README.md](README.md) for technical documentation
- [ ] Explore [ARCHITECTURE.txt](ARCHITECTURE.txt) for system overview
- [ ] Create a real client with actual data
- [ ] Set up production deployment (if needed)

## Common Commands ✓

```bash
# Start everything (automated)
cd frontend && ./start.sh

# Backend only
cd frontend/backend
source venv/bin/activate
python main.py

# Frontend only
cd frontend
npm run dev

# Build for production
cd frontend
npm run build

# Run linter
cd frontend
npm run lint

# Type check
cd frontend
npx tsc --noEmit

# View API docs
open http://localhost:8000/docs

# Access frontend
open http://localhost:5173
```

## Success Indicators ✓

You know everything is working when:

✅ Both servers start without errors
✅ Green "Live" indicator shows in UI sidebar
✅ API health check returns OK
✅ Client onboarding creates directories
✅ Task creation shows in task list
✅ Toast notifications appear
✅ Agent list loads 20+ agents
✅ Configuration page shows settings
✅ No errors in browser console
✅ No errors in terminal logs

## Getting Help ✓

If you're still having issues:

1. Check browser console (F12) for frontend errors
2. Check terminal for backend errors
3. Review [README.md](README.md) troubleshooting section
4. Verify all prerequisites are met
5. Try restarting both servers
6. Clear browser cache and reload

## Completion ✓

- [ ] All checks above passed
- [ ] Test client onboarded successfully
- [ ] Test task created successfully
- [ ] Agents page loads correctly
- [ ] WebSocket shows "Live"
- [ ] No errors in console or terminal

**Congratulations! Your SEO-SWARM frontend is ready to use.** 🎉

Start onboarding real clients and managing your agent workflows!
