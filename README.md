# HybridWorkspace Control Plane

**Plataforma de Gestão Unificada de Ambientes Remotos e Híbridos com Zero Trust**

[![CI/CD](https://github.com/Alfredoprogramador/HybridWorkspace-Control-Plane/actions/workflows/ci.yml/badge.svg)](https://github.com/Alfredoprogramador/HybridWorkspace-Control-Plane/actions/workflows/ci.yml)
[![Security Scan](https://github.com/Alfredoprogramador/HybridWorkspace-Control-Plane/actions/workflows/security.yml/badge.svg)](https://github.com/Alfredoprogramador/HybridWorkspace-Control-Plane/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A central control platform (Control Plane) implementing Zero Trust Architecture (NIST 800-207) for managing hybrid work environments at enterprise scale.

---

## Overview

With the permanent hybrid work model, enterprises face complex challenges: inconsistent security across personal and corporate devices, difficulty applying uniform policies, low visibility into device posture, and risk of data leakage. HybridWorkspace Control Plane solves these by providing a **unified Zero Trust management platform**.

### Key Features

- 🔐 **Zero Trust Architecture** — Never trust, always verify (NIST 800-207 / BeyondCorp)
- 📱 **Device Management** — Posture monitoring across Windows, macOS, Linux, iOS, Android
- 🛡️ **Policy as Code** — OPA (Open Policy Agent) + Rego for centralized policy management
- 🌐 **Secure VPN** — Self-hosted Tailscale (Headscale) + WireGuard
- 📊 **Security Dashboard** — Real-time posture visibility and compliance tracking
- 🤖 **AI Threat Detection** — Behavioral anomaly detection with LangGraph
- 🔗 **SSO Integration** — Microsoft Entra ID, Google Workspace, SAML
- 🔄 **GitOps** — Kubernetes + ArgoCD for infrastructure management
- 📈 **Observability** — OpenTelemetry + Grafana + Loki + Tempo

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Control Plane (FastAPI)                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Identity  │  │  Device    │  │ Policy   │  │  Audit     │  │
│  │  Service   │  │  Registry  │  │ Engine   │  │  Service   │  │
│  │  (SSO+MFA) │  │  (MDM)     │  │ (OPA)    │  │  (SIEM)    │  │
│  └────────────┘  └────────────┘  └──────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────┘
           │                │                │
     ┌─────▼──┐      ┌──────▼───┐     ┌─────▼──────┐
     │Frontend│      │  Device  │     │    VPN     │
     │Next.js │      │  Agents  │     │ (Headscale)│
     │Dashboard│     │(Go/Python)│    │ WireGuard  │
     └────────┘      └──────────┘     └────────────┘
```

### Trust Levels

| Score | Level | Access |
|-------|-------|--------|
| ≥ 90% | 🟢 **TRUSTED** | Full access |
| 60–89% | 🟡 **CONDITIONAL** | Limited access |
| < 60% | 🔴 **UNTRUSTED** | Access blocked |

---

## Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui |
| **Backend** | Python 3.12 + FastAPI + Pydantic v2 |
| **Database** | PostgreSQL + TimescaleDB + Redis |
| **Zero Trust / VPN** | Tailscale + Headscale (self-hosted) + WireGuard |
| **Device Agents** | Go (Windows/macOS/Linux), Osquery |
| **Policy Engine** | OPA (Open Policy Agent) + Rego |
| **AI / Analytics** | LangGraph + custom anomaly detection |
| **Infrastructure** | Kubernetes + Terraform + ArgoCD |
| **Observability** | OpenTelemetry + Grafana + Loki + Tempo |
| **CI/CD** | GitHub Actions |

---

## Project Structure

```
hybrid-workspace-control-plane/
├── apps/
│   ├── frontend/              # Next.js 15 dashboard
│   ├── desktop-agent/         # Electron + Osquery desktop app
│   └── backend/               # FastAPI Control Plane API
├── packages/
│   ├── shared/                # Shared TypeScript types & utilities
│   ├── zero-trust/            # Zero Trust evaluation logic
│   ├── collaboration/         # LiveKit + Y.js real-time
│   └── ai-policies/           # OPA Rego policies + LangGraph
├── agents/
│   └── device-agent/          # Go device agent (posture reporting)
├── infra/
│   ├── terraform/             # Infrastructure as Code
│   └── kubernetes/            # Kubernetes manifests
├── docs/
│   ├── zero-trust-model.md    # ZTA architecture documentation
│   └── privacy-policy.md      # Employee privacy policy
├── docker-compose.yml         # Local development environment
└── .github/workflows/         # CI/CD pipelines
```

---

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+
- Go 1.23+
- Docker & Docker Compose
- npm 10+

### 1. Clone and install dependencies

```bash
git clone https://github.com/Alfredoprogramador/HybridWorkspace-Control-Plane.git
cd HybridWorkspace-Control-Plane

# Install Node.js dependencies (all packages)
npm install

# Install Python dependencies
cd apps/backend && pip install -r requirements.txt && pip install -r requirements-dev.txt && cd ../..
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start local infrastructure

```bash
# Start all services (PostgreSQL, Redis, OPA, Grafana, etc.)
docker-compose up -d postgres redis opa otel-collector grafana
```

### 4. Start development servers

```bash
# Start all apps in development mode
npm run dev

# Or start individually:
# Backend: cd apps/backend && uvicorn app.main:app --reload
# Frontend: cd apps/frontend && npm run dev
```

### 5. Access the platform

| Service | URL |
|---------|-----|
| Dashboard (Frontend) | http://localhost:3000 |
| API (Backend) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/api/docs |
| Grafana | http://localhost:3001 |
| OPA | http://localhost:8181 |

---

## Development

### Running Tests

```bash
# All tests
npm test

# Backend tests only
cd apps/backend && pytest -v

# Frontend tests only
cd apps/frontend && npm test

# OPA policy tests
opa test packages/ai-policies/rego/ -v
```

### Building the Device Agent

```bash
cd agents/device-agent

# Build for current platform
go build -o hwcp-agent ./...

# Cross-compile for all platforms
GOOS=linux GOARCH=amd64 go build -o hwcp-agent-linux-amd64 ./...
GOOS=darwin GOARCH=arm64 go build -o hwcp-agent-darwin-arm64 ./...
GOOS=windows GOARCH=amd64 go build -o hwcp-agent-windows-amd64.exe ./...
```

### Enrolling a Device

```bash
# Get enrollment token from the Control Plane dashboard
# Then on the device:
hwcp-agent enroll --token <enrollment-token> --server https://api.company.com

# Start the agent
hwcp-agent start
```

---

## Security

This platform is built on security-first principles:

- All API endpoints require authentication (JWT tokens with 30-minute expiry)
- Security headers applied to all responses (HSTS, CSP, X-Frame-Options, etc.)
- All requests logged for audit purposes
- Secrets managed via environment variables (never hardcoded)
- Regular automated security scans via GitHub Actions (Trivy, CodeQL, TruffleHog)

See [docs/zero-trust-model.md](docs/zero-trust-model.md) for the full ZTA architecture documentation.

---

## Privacy

We take employee privacy seriously. The platform collects only what is strictly necessary for security:

- ✅ Device security posture (encryption, firewall, AV)
- ✅ Authentication and access logs
- ❌ Personal files or browsing history
- ❌ Keystrokes or screen recording (without explicit consent)

See [docs/privacy-policy.md](docs/privacy-policy.md) for full details.

---

## Roadmap

### MVP – Phase 1 (8 weeks)
- [x] Device enrollment with lightweight agent
- [x] Zero Trust authentication (SSO + Device Posture)
- [x] Always-on VPN (Tailscale)
- [x] Basic access policies (user, group, location)
- [x] Device and security status dashboard
- [ ] Microsoft Entra ID / Google Workspace integration

### Phase 2 – Advanced (12 weeks)
- [ ] Continuous posture verification
- [ ] Real-time collaboration (LiveKit + Y.js)
- [ ] Session recording (with consent)
- [ ] AI-based behavioral threat detection
- [ ] Contextual policies (network-aware)

### Phase 3 – Enterprise (12 weeks)
- [ ] Multi-tenancy and subsidiary support
- [ ] Full MDM (remote wipe, app management)
- [ ] DLP integration
- [ ] Compliance reports (LGPD, ISO 27001, SOC 2)
- [ ] Self-service portal for employees
- [ ] Shadow IT detection

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure all tests pass and security scans are clean before submitting a PR.

---

## License

MIT License – see [LICENSE](LICENSE) for details.
