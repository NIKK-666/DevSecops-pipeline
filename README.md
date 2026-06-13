# Automated DevSecOps Security Gate Pipeline

A robust, continuous integration pipeline built with **GitHub Actions** designed to systematically enforce shift-left security practices. This workflow automates vulnerability tracking, catches hardcoded secrets, and screens software dependencies for public vulnerabilities on every code push or pull request.

---

## 🏗️ Architecture & Security Scanners

The pipeline implements a multi-tiered security gate utilizing three distinct open-source scanning tools to produce comprehensive security telemetry:

```
      [ Developer Git Push / Pull Request ]
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│               GitHub Actions Workflow                  │
├───────────────────┬───────────────────┬────────────────┤
│    Job 1: SAST    │    Job 2: SCA     │ Job 3: Secrets │
│    (Semgrep)      │     (Trivy)       │   (Gitleaks)   │
└─────────┬─────────┴─────────┬─────────┴────────┬───────┘
          │                   │                  │
          ▼                   ▼                  ▼
   (SARIF Report)      (SARIF Report)     (History Scan)
          │                   │                  │
          └───────────────────┼──────────────────┘
                              ▼
                ┌───────────────────────────┐
                │   GitHub Security Tab     │
                │  (Centralized Dashboard)  │
                └─────────────┬─────────────┘
                              │
                              ▼
        [ Enforced Branch Protection Rules Evaluated ]
          ├── IF Security Violations Found ──> [ MERGE BLOCKED ]
          └── IF All Checks Pass          ──> [ ALLOW MERGE ]

```

### 1. Static Application Security Testing (SAST) — Semgrep

* 
**Purpose:** Inspects source code to trace data flows and isolate behavioral patterns that point to critical design flaws.


* 
**Core Function:** Scans for application-layer flaws such as SQL Injections and dangerous command executions.


* 
**Reporting:** Formats execution telemetry into standardized **SARIF** (Static Analysis Results Interchange Format) logs, instantly parsing the findings straight into GitHub's native Code Scanning dashboard.



### 2. Software Composition Analysis (SCA) — Trivy

* 
**Purpose:** Scans the project file-system to build a dependency inventory tree and cross-reference public CVE databases.


* 
**Core Function:** Targets third-party library tracking hazards, flagging legacy dependencies embedded with known vulnerabilities.


* 
**Fail Gate:** Programmed to trigger an exit code (`exit-code: 1`) on high-risk findings, systematically breaking the build step to stop problematic payloads from expanding.



### 3. Secrets Detection — Gitleaks

* 
**Purpose:** Prevents credential leakage by scanning git history for hardcoded signatures.


* 
**Core Function:** Uses regex matching to inspect past commits for tracking hazards like plaintext passwords, high-entropy API tokens, or AWS access vectors.


* 
**Depth:** Configured with a deep repository clone strategy (`fetch-depth: 0`) to audit structural changes throughout historical timelines rather than just current file snapshots.



---

## 🛡️ Enforcing Branch Protection Rules

To elevate this workflow from a monitoring utility into a defensive quality gate, the pipeline integrates with GitHub's branch protection policies:

1. 
**Mandatory Build Passing:** Merging into the protected target branch is programmatically blocked unless all security scanning jobs finish cleanly with a zero failure status.


2. 
**Left-Shift Validation:** Developers receive real-time, granular feedback on security flaws inside their pull requests before modifications get introduced into production lines.



---

## ⚙️ Custom Semgrep Policy Enforcement

This project implements organizational security configurations via custom Semgrep detection definitions (`rules/no-os-system.yml`). This specific gate actively bans weak shell hooks like Python's `os.system()` to eliminate command injection opportunities and forces developers toward more secure alternatives like `subprocess.run()`:

```yaml
# rules/no-os-system.yml
rules:
  - id: detect-insecure-os-system
    pattern: os.system(...)
    message: "CRITICAL: Insecure os.system() execution detected. This pattern is vulnerable to command injection. Refactor using subprocess.run()."
    languages: [python]
    severity: ERROR
    metadata:
      category: security
      confidence: HIGH

```

---

## 🧪 Validating with a Target Footprint

The pipeline’s alert logic was rigorously tested using an intentionally broken Python component designed to simulate classic application risks:

```python
import os
import mysql.connector

# 1. SQL Injection Vector (Caught by Semgrep)
def get_user_data(user_input):
    cursor.execute(f"SELECT * FROM accounts WHERE id = '{user_input}'")

# 2. Command Injection Vector (Caught by Custom Semgrep Rule)
def network_diagnostic(host_ip):
    os.system(f"ping -c 1 {host_ip}")

# 3. Hardcoded Secret Leak (Caught by Gitleaks)
AWS_PRODUCTION_KEY = "AKIAIOSFODNN7EXAMPLE" 

```

---

## 📊 Key Takeaways & Learnings

* 
**Shift-Left Implementation:** Standardized security checks directly inside developer build cycles to minimize the lifecycle cost of software remediation.


* 
**Unified Dashboard Ingestion:** Centralized disparate data logs (SAST/SCA) into a single, high-fidelity native view utilizing standard SARIF outputs.


* 
**Declarative Control:** Codified security constraints as immutable, versioned infrastructure components using GitHub Actions YAML definitions.


  <img width="663" height="448" alt="image" src="https://github.com/user-attachments/assets/1439bd3e-adbd-4b07-99e8-4ea0c20f8af0" />

