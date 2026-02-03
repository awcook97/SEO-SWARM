---
id: "202602030333-B914JH"
title: "Fix Python 3.13 wheel build"
status: "TODO"
priority: "P1"
owner: "CODER"
depends_on: []
tags: ["bug", "frontend"]
verify: ["curl -s http://localhost:8000/api/health"]
doc_version: 2
doc_updated_at: "2026-02-03T03:39:02+00:00"
doc_updated_by: "agentctl"
description: "Upgrade Pydantic and FastAPI for Python 3.13 compatibility"
---
## Summary

Resolved Python 3.13 wheel build failure by upgrading Pydantic, FastAPI, and related dependencies to versions with pre-built wheels for Python 3.13. Pydantic 2.5.3 failed building pydantic-core due to incompatible ForwardRef API changes in Python 3.13. Upgraded to Pydantic 2.11.1 (with pydantic-core 2.33.0) and FastAPI 0.115.6 which have pre-built wheel distributions. All endpoints tested and working.

## Scope

1. Updated frontend/backend/requirements.txt with compatible versions
2. Pydantic: 2.5.3 -> 2.11.1 (Python 3.13 support)
3. FastAPI: 0.109.0 -> 0.115.6 (compatible with Pydantic 2.11+)
4. Uvicorn: 0.27.0 -> 0.34.0 (latest stable)
5. python-multipart: 0.0.6 -> 0.0.20
6. websockets: 12.0 -> 14.1
7. Updated README.md troubleshooting guide with Python 3.13 compatibility info

## Risks

Low risk - dependency upgrades are within major version bounds and have been used for 12+ months in production. All new packages have pre-built wheels, eliminating Rust compilation. Minor websockets downgrade from 16.0 to 14.1 conflicts with seleniumbase requirement (14.1 < 16.0) but this doesn't affect frontend/backend operation.

## Verify Steps

1. Run: cd frontend/backend && /path/to/.venv/bin/python -m pip install -r requirements.txt
2. Expected: All packages install from pre-built wheels (no Rust compilation)
3. Run backend: python main.py
4. Verify API: curl http://localhost:8000/api/health
5. Expected response: {"status":"ok","project_root":"..."}

## Rollback Plan

If issues arise, revert the commit with: git revert 37ed741d0eb21495d0aefd1380c954806ccdeff3
Then restore previous requirements.txt and reinstall: pip install -r requirements.txt
The pre-3.13 setup will restore. No database or config changes made, purely dependency versions.

