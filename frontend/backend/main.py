#!/usr/bin/env python3
"""FastAPI backend for SEO-SWARM agent management UI."""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="SEO-SWARM API", version="1.0.0")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
AGENTCTL_PATH = PROJECT_ROOT / ".codex-swarm" / "agentctl.py"
AGENTS_DIR = PROJECT_ROOT / ".codex-swarm" / "agents"
CONFIG_PATH = PROJECT_ROOT / ".codex-swarm" / "config.json"
TASKS_PATH = PROJECT_ROOT / ".codex-swarm" / "tasks.json"


# Pydantic models
class ClientOnboard(BaseModel):
    name: str
    slug: str
    website: str | None = None
    crawl_site: bool = False


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str = "med"
    owner: str = "ORCHESTRATOR"
    depends_on: list[str] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: str | None = None
    owner: str | None = None
    status: str | None = None


class ConfigUpdate(BaseModel):
    key: str
    value: str | int | bool | list | dict
    is_json: bool = False


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


def run_agentctl(args: list[str]) -> dict[str, Any]:
    """Run agentctl.py and return parsed output."""
    cmd = [sys.executable, str(AGENTCTL_PATH)] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }


def run_script(script_path: Path, args: list[str]) -> dict[str, Any]:
    """Run a Python script and return parsed output."""
    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }


# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "project_root": str(PROJECT_ROOT)}


# Config endpoints
@app.get("/api/config")
async def get_config():
    """Get current configuration."""
    try:
        if not CONFIG_PATH.exists():
            raise HTTPException(status_code=404, detail="Config file not found")
        config = json.loads(CONFIG_PATH.read_text())
        return {"success": True, "config": config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/config")
async def update_config(update: ConfigUpdate):
    """Update a configuration value."""
    args = ["config", "set", update.key, str(update.value)]
    if update.is_json:
        args.append("--json")
    
    result = run_agentctl(args)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "config_updated", "key": update.key})
    return result


# Agent endpoints
@app.get("/api/agents")
async def list_agents():
    """List all available agents."""
    try:
        if not AGENTS_DIR.exists():
            return {"agents": []}
        
        agents = []
        for agent_file in AGENTS_DIR.glob("*.json"):
            try:
                agent_data = json.loads(agent_file.read_text())
                agents.append({
                    "name": agent_file.stem,
                    "file": agent_file.name,
                    **agent_data
                })
            except Exception:
                pass
        
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents/{agent_name}")
async def get_agent(agent_name: str):
    """Get specific agent details."""
    try:
        agent_file = AGENTS_DIR / f"{agent_name}.json"
        if not agent_file.exists():
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        agent_data = json.loads(agent_file.read_text())
        return {"agent": agent_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Task endpoints
@app.get("/api/tasks")
async def list_tasks():
    """List all tasks."""
    result = run_agentctl(["task", "list", "--json"])
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["stderr"])
    
    try:
        # Parse JSON from stdout
        tasks_data = json.loads(result["stdout"]) if result["stdout"].strip() else {"tasks": []}
        return tasks_data
    except json.JSONDecodeError:
        # Fallback to reading tasks.json directly
        if TASKS_PATH.exists():
            return json.loads(TASKS_PATH.read_text())
        return {"tasks": []}


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Get specific task details."""
    result = run_agentctl(["task", "show", task_id])
    if not result["success"]:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return {"task_id": task_id, "output": result["stdout"]}


@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    """Create a new task."""
    args = [
        "task", "new",
        "--title", task.title,
        "--description", task.description,
        "--priority", task.priority,
        "--owner", task.owner,
    ]
    
    result = run_agentctl(args)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "task_created", "output": result["stdout"]})
    return result


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, task: TaskUpdate):
    """Update an existing task."""
    args = ["task", "update", task_id]
    
    if task.title:
        args.extend(["--title", task.title])
    if task.description:
        args.extend(["--description", task.description])
    if task.priority:
        args.extend(["--priority", task.priority])
    if task.owner:
        args.extend(["--owner", task.owner])
    
    result = run_agentctl(args)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "task_updated", "task_id": task_id})
    return result


@app.post("/api/tasks/{task_id}/start")
async def start_task(task_id: str):
    """Mark task as started."""
    result = run_agentctl(["start", task_id, "--author", "USER", "--body", "Started via UI"])
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "task_started", "task_id": task_id})
    return result


@app.post("/api/tasks/{task_id}/finish")
async def finish_task(task_id: str, commit: str, author: str = "USER"):
    """Mark task as finished."""
    result = run_agentctl([
        "finish", task_id,
        "--commit", commit,
        "--author", author,
        "--body", "Finished via UI"
    ])
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "task_finished", "task_id": task_id})
    return result


# Client onboarding endpoints
@app.post("/api/clients/onboard")
async def onboard_client(client: ClientOnboard):
    """Onboard a new client."""
    script_path = PROJECT_ROOT / "scripts" / "workflow" / "swarm_workflow.py"
    
    args = [
        "--client", client.name,
        "--slug", client.slug,
    ]
    
    if client.website:
        args.extend(["--site-url", client.website])
    
    result = run_script(script_path, args)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["stderr"])
    
    await manager.broadcast({"type": "client_onboarded", "slug": client.slug})
    return result


@app.get("/api/clients")
async def list_clients():
    """List all clients."""
    try:
        outputs_dir = PROJECT_ROOT / "data" / "outputs"
        if not outputs_dir.exists():
            return {"clients": []}
        
        clients = []
        for client_dir in outputs_dir.iterdir():
            if client_dir.is_dir():
                inputs_file = client_dir / "inputs.md"
                clients.append({
                    "slug": client_dir.name,
                    "has_inputs": inputs_file.exists(),
                    "path": str(client_dir.relative_to(PROJECT_ROOT))
                })
        
        return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/clients/{slug}/outputs")
async def get_client_outputs(slug: str):
    """Get all outputs for a client."""
    try:
        client_dir = PROJECT_ROOT / "data" / "outputs" / slug
        if not client_dir.exists():
            raise HTTPException(status_code=404, detail=f"Client {slug} not found")
        
        outputs = {
            "reports": [],
            "pages": [],
            "articles": [],
            "social": [],
            "email": []
        }
        
        for category in outputs.keys():
            category_dir = client_dir / category
            if category_dir.exists():
                outputs[category] = [
                    {
                        "name": f.name,
                        "path": str(f.relative_to(PROJECT_ROOT))
                    }
                    for f in category_dir.iterdir()
                    if f.is_file()
                ]
        
        return {"slug": slug, "outputs": outputs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back for testing
            await websocket.send_json({"type": "echo", "message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Serve frontend static files in production
try:
    frontend_dist = Path(__file__).parent.parent / "dist"
    if frontend_dist.exists():
        app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static")
except Exception:
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
