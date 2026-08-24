# SecurePipe Lite DevSecOps Pipeline

## Security Pipeline

```mermaid
flowchart TD
    CODE[Source Code]

    CODE --> PR[Pull Request]

    PR --> GITLEAKS[Gitleaks<br/>Secret Scanning]

    GITLEAKS -->|Pass| SEMGREP[Semgrep<br/>SAST]
    GITLEAKS -->|Fail| BLOCK1[Block Pipeline]

    SEMGREP -->|Pass| PIPAUDIT[pip-audit<br/>Dependency Scanning]
    SEMGREP -->|Fail| BLOCK2[Block Pipeline]

    PIPAUDIT -->|Pass| TESTS[Automated Tests]
    PIPAUDIT -->|Fail| BLOCK3[Block Pipeline]

    TESTS -->|Pass| BUILD[Docker Build]
    TESTS -->|Fail| BLOCK4[Block Pipeline]

    BUILD --> TRIVY[Trivy<br/>Container Vulnerability Scan]

    TRIVY -->|Pass| APPROVED[Approved Artifact]
    TRIVY -->|Fail| BLOCK5[Block Pipeline]

    APPROVED --> GHCR[GitHub Container Registry]

    GHCR --> DEPLOY[Versioned Deployment]
```

## Security Gates

```text
                    SECUREPIPE LITE

Developer
    |
    v
Feature Branch
    |
    v
Pull Request
    |
    v
+-------------------------------+
| Gitleaks                      |
| Secret Detection              |
+-------------------------------+
    |
    v
+-------------------------------+
| Semgrep                       |
| Static Application Security   |
+-------------------------------+
    |
    v
+-------------------------------+
| pip-audit                     |
| Dependency Vulnerabilities    |
+-------------------------------+
    |
    v
+-------------------------------+
| Automated Tests               |
| Functional Validation         |
+-------------------------------+
    |
    v
+-------------------------------+
| Docker Build                  |
+-------------------------------+
    |
    v
+-------------------------------+
| Trivy                         |
| Container Vulnerabilities     |
+-------------------------------+
    |
    v
Required CI Check
    |
    v
Merge Allowed
    |
    v
GHCR
    |
    v
Versioned Release
```

## Shift-Left Security

Security validation happens before deployment.

A finding in a required security stage causes the CI job to fail, preventing the protected pull request from being merged until the issue is remediated.

The project currently demonstrates:

- Secret scanning with Gitleaks
- SAST with Semgrep
- Software Composition Analysis with pip-audit
- Automated regression testing
- Container vulnerability scanning with Trivy
- Non-root container execution
- Immutable GitHub Actions references
- GitHub Secrets
- Protected branch enforcement
- Versioned container artifacts
- Deployment rollback