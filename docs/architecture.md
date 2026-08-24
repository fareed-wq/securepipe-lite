# SecurePipe Lite Architecture

## System Architecture

```mermaid
flowchart LR
    DEV[Developer]

    subgraph GitHub
        REPO[GitHub Repository]
        ACTIONS[GitHub Actions]
        GHCR[GitHub Container Registry]
    end

    subgraph Security Pipeline
        GL[Gitleaks]
        SG[Semgrep]
        PA[pip-audit]
        TEST[Automated Tests]
        BUILD[Docker Build]
        TRIVY[Trivy]
    end

    subgraph Deployment
        COMPOSE[Docker Compose]
        TOFU[OpenTofu]
        DOCKER[Docker Engine]
    end

    subgraph Application
        API[FastAPI]
        HEALTH[/health]
        METRICS[/metrics]
        LOGS[Structured JSON Logs]
    end

    DEV -->|Git Push / PR| REPO
    REPO --> ACTIONS

    ACTIONS --> GL
    GL --> SG
    SG --> PA
    PA --> TEST
    TEST --> BUILD
    BUILD --> TRIVY

    TRIVY -->|Security Gate Passed| GHCR

    GHCR --> COMPOSE
    GHCR --> TOFU

    COMPOSE --> DOCKER
    TOFU --> DOCKER

    DOCKER --> API

    API --> HEALTH
    API --> METRICS
    API --> LOGS
```

## Delivery Model

SecurePipe Lite separates build and deployment responsibilities.

```text
SOURCE
  |
  v
GitHub Repository
  |
  v
CI + Security Validation
  |
  v
Docker Image
  |
  v
Container Vulnerability Scan
  |
  v
GHCR
  |
  v
Immutable Versioned Image
  |
  +-------------------+
  |                   |
  v                   v
Docker Compose      OpenTofu
  |                   |
  +---------+---------+
            |
            v
       Docker Engine
            |
            v
        FastAPI App
```

The deployment system consumes previously validated container images rather than rebuilding application source code on the deployment host.