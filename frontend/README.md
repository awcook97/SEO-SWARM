# SEO-SWARM Frontend

Modern web dashboard for managing the SEO-SWARM agent workflow system.

## Features

- **Client Onboarding Wizard**: Step-by-step setup for new clients with automatic scaffolding
- **Task Management**: Create, track, and manage tasks across the agent swarm
- **Agent Registry**: View all available agents and their roles
- **Real-time Updates**: WebSocket integration for live progress monitoring
- **Client Outputs Browser**: Explore generated reports, pages, and content
- **Configuration Manager**: Edit workflow settings and system configuration

## Tech Stack

### Backend
- **FastAPI**: High-performance Python API framework
- **Uvicorn**: ASGI server with WebSocket support
- **Pydantic**: Data validation and settings management

### Frontend
- **React 18**: Modern UI library with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tooling
- **TailwindCSS**: Utility-first styling
- **React Query**: Server state management
- **Zustand**: Client state management
- **React Router**: Client-side routing
- **Lucide React**: Icon library

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd frontend/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- WebSocket: `ws://localhost:8000/ws`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Production Build

```bash
# Build frontend for production
cd frontend
npm run build

# The built files will be in frontend/dist/
# The FastAPI server will automatically serve them
```

## Project Structure

```
frontend/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Layout.tsx       # Main layout with sidebar
│   │   ├── Button.tsx       # Button component
│   │   ├── Input.tsx        # Input component
│   │   ├── Card.tsx         # Card container
│   │   └── LoadingSpinner.tsx
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx    # Main dashboard
│   │   ├── ClientOnboarding.tsx
│   │   ├── TaskManagement.tsx
│   │   ├── AgentViewer.tsx
│   │   ├── ClientOutputs.tsx
│   │   └── Configuration.tsx
│   ├── lib/                 # Utilities and helpers
│   │   ├── api.ts          # API client functions
│   │   ├── store.ts        # Zustand state management
│   │   ├── websocket.ts    # WebSocket hook
│   │   └── utils.ts        # Helper functions
│   ├── App.tsx             # Root component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## API Endpoints

### Health & Config
- `GET /api/health` - Health check
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

### Agents
- `GET /api/agents` - List all agents
- `GET /api/agents/{name}` - Get agent details

### Tasks
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{id}` - Get task details
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task
- `POST /api/tasks/{id}/start` - Start task
- `POST /api/tasks/{id}/finish` - Finish task

### Clients
- `POST /api/clients/onboard` - Onboard new client
- `GET /api/clients` - List all clients
- `GET /api/clients/{slug}/outputs` - Get client outputs

### WebSocket
- `WS /ws` - Real-time updates and notifications

## Development

### Running Tests

```bash
# Backend tests (if implemented)
cd frontend/backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

### Linting

```bash
# Frontend linting
cd frontend
npm run lint
```

### Type Checking

```bash
# TypeScript type checking
cd frontend
npx tsc --noEmit
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Docker Deployment

Create a `Dockerfile` in the frontend directory:

```dockerfile
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./backend/
COPY --from=frontend-build /app/dist ./dist
EXPOSE 8000
CMD ["python", "backend/main.py"]
```

Build and run:

```bash
docker build -t seo-swarm-ui .
docker run -p 8000:8000 -v $(pwd)/../..:/workspace seo-swarm-ui
```

## Usage Guide

### Onboarding a New Client

1. Navigate to **Onboard Client** from the sidebar
2. Fill in client information:
   - **Client Name**: Full business name
   - **Slug**: URL-friendly identifier (auto-generated)
   - **Website**: Optional website URL
   - **Crawl Site**: Check to cache HTML during setup
3. Click **Onboard Client**
4. The system will:
   - Create directory structure
   - Scaffold template files
   - Optionally crawl and cache the website
   - Pre-fill inputs.md

### Managing Tasks

1. Navigate to **Tasks** from the sidebar
2. Click **New Task** to create a task
3. Fill in task details:
   - Title and description
   - Priority (low/med/high)
   - Owner (agent role)
4. Track task status with filters
5. Start tasks by clicking the **Start** button

### Viewing Agents

1. Navigate to **Agents** from the sidebar
2. Browse agents by category
3. View agent roles and descriptions

### Monitoring Progress

- The sidebar shows live connection status
- Toast notifications appear for important events
- Dashboard shows real-time task counts
- WebSocket automatically reconnects on disconnect

## Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Check that port 8000 is available
- Verify all dependencies are installed: `pip list`

### Frontend won't start
- Ensure Node.js 18+ is installed
- Delete `node_modules` and run `npm install` again
- Check that port 5173 is available

### WebSocket connection fails
- Verify backend is running
- Check browser console for errors
- Ensure no firewall is blocking WebSocket connections

### API calls fail
- Check backend logs for errors
- Verify the agentctl.py path is correct
- Ensure project root path is properly configured

## Contributing

1. Follow TypeScript best practices
2. Use functional components with hooks
3. Keep components small and focused
4. Add proper error handling
5. Test WebSocket functionality
6. Maintain responsive design

## License

Same as the parent SEO-SWARM project.
