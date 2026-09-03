# GRC NIST 800-171 Tool

Web-based Governance, Risk & Compliance application for NIST SP 800-171 Rev 2 gap analysis and professional C-suite reporting.

**Tech Stack**
- Backend: FastAPI + SQLite
- Frontend: React (Vite) + TypeScript + Tailwind
- Auth: Simple local username/password
- Reports: Professional PDF (pie chart, executive summary, recommended actions)

See `.hermes/plans/grc-nist-800-171-plan.md` for the full locked spec.

## Quick Start (Windows PowerShell)
1. Backend: See `backend/run.cmd` or manual uvicorn
2. Frontend: `cd frontend && npm install && npm run dev`

Repo created: 2026-09-03
