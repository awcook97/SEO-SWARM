---
id: "202601150500-5PE365"
title: "HighPoint HVAC: 14-day daily social posting pack"
status: "TODO"
priority: "P1"
owner: "ORCHESTRATOR"
depends_on: []
tags: ["seo", "content", "social"]
verify: [".venv/bin/python scripts/swarm_workflow.py --help"]
doc_version: 2
doc_updated_at: "2026-01-15T05:00:10+00:00"
doc_updated_by: "agentctl"
description: "Create a 14-day daily posting calendar with city-targeted variants and rotating service focus (Air Duct, Dryer Vent, Chimney, AC Cleaning, and related chimney add-ons) across Instagram/Facebook/Nextdoor/LinkedIn/X/GBP, using placeholders for links/media."
---

# Summary

Create a 14-day daily social posting pack for HighPoint HVAC across Instagram, Facebook, Nextdoor, LinkedIn, X, and Google Business Profile, with city-targeted variants and rotating service focus.

# Context

- Approved business facts and service list: `outputs/highpoint/inputs.md`
- Daily calendar: `outputs/highpoint/social/daily-calendar.md`
- Platform-ready copy: `outputs/highpoint/social/social-posts.md`
- Workflow context: `docs/seo/swarm-execution-workflow.md`

# Scope

- Produce 14 days of posts across 6 platforms per day (with placeholders for links/UTMs/media).
- Rotate focus across primary services and related add-ons.
- City-target each day to a different service area from the approved list.

# Risks

- Posts include placeholders for links/UTMs/media and must be finalized before publishing.
- Avoid adding unverified claims (reviews, certifications, guarantees, “best/#1”, etc.) until sources are approved.

# Verify Steps

- Confirm `outputs/highpoint/social/daily-calendar.md` contains 14 days with a city + service rotation.
- Confirm `outputs/highpoint/social/social-posts.md` includes 14 day sections with per-platform variants.

# Rollback Plan

- Delete `outputs/highpoint/social/` locally if needed (folder is ignored by git).
- Revert any committed tracked artifacts via `git revert <commit>`.

# Notes

- Calendar uses these 14 cities: Denver, Colorado Springs, Fort Collins, Aurora, Boulder, Highlands Ranch, Centennial, Littleton, Castle Rock, Westminster, Greenwood Village, Lafayette, Longmont, Parker.
