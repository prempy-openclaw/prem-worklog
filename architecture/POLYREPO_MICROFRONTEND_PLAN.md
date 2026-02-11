# Polyrepo + Micro-frontend Migration Plan

Owner: Prem + Team

## Target Services (1:1 repo)
1. `prem-home-shell` — central portal/container + global navigation
2. `prem-money-manager` — existing Money Manager app (API + UI)
3. `prem-agent-monitor` — Agent Monitor app (UI + monitoring API adapter)

## Runtime Topology
- `/` -> Home Shell
- `/money` -> Money Manager UI
- `/monitor` -> Agent Monitor UI
- `/api/money/*` -> Money Manager API
- `/api/monitor/*` -> Agent Monitor API

## Migration Phases
- **20%**: Architecture + repo boundaries + routing contract
- **40%**: Create 3 separated local service folders and independent Dockerfiles
- **60%**: Add independent CI/CD workflows per service
- **80%**: Reverse proxy/API gateway routing + integrated smoke test
- **100%**: Split git repos, push to GitHub, update architecture diagram/docs

## DoD Mapping
- Repo split complete (1 repo / service)
- Home links + navigation work seamlessly
- Independent deployment verified per service
- Architecture diagram + runbook updated
