# CryptoSights Deployment Guide

## Overview

This comprehensive guide details the architecture, containerization strategy, and deployment workflow for **CryptoSights**—a stateful NLP-based web application designed for large-scale cryptocurrency text analysis and retrieval.

**Intended Audience:** Developers responsible for deployment, maintenance, or extension of the CryptoSights platform.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Containerization Strategy](#containerization-strategy)
4. [Application Entry Point](#application-entry-point)
5. [Container Structure](#container-structure)
6. [Dependency Management](#dependency-management)
7. [Resource Requirements](#resource-requirements)
8. [Deployment Platform](#deployment-platform)
9. [Network Configuration](#network-configuration)
10. [Deployment Workflow](#deployment-workflow)
11. [Monitoring and Debugging](#monitoring-and-debugging)
12. [CI/CD Pipeline](#cicd-pipeline)
13. [Best Practices](#best-practices)

---

## System Architecture

CryptoSights is engineered to perform sophisticated natural language processing operations on cryptocurrency-related content:

### Core Capabilities

- **Large-Scale Text Indexing** — Processes and indexes substantial text corpora
- **NLP Preprocessing & Analysis** — Performs sentence-level linguistic analysis
- **Query-Based Retrieval** — Implements BM25 algorithm for information retrieval
- **Runtime Self-Improvement** — Continuously updates and optimizes through runtime feedback

### Architectural Characteristics

The application maintains **persistent state** across sessions and requires:

- High-memory allocation for in-memory indexes
- Persistent filesystem for saved artifacts
- Long-running background processes
- Stateful session management

---

## Technology Stack

### Core Technologies

- **Runtime:** Python 3.10
- **Web Framework:** Flask
- **NLP Libraries:** NLTK, custom preprocessing modules
- **Retrieval Algorithm:** BM25 (Okapi BM25)
- **Containerization:** Docker
- **Deployment Platform:** Hugging Face Spaces

### Key Dependencies

- Flask for web serving
- NLTK for natural language processing
- Pickle for index serialization
- Subprocess module for process management

---

## Containerization Strategy

### Why Docker?

Docker containerization provides critical advantages for CryptoSights:

#### Environment Consistency
- Guarantees identical behavior across development, staging, and production
- Eliminates "works on my machine" scenarios
- Ensures reproducible builds

#### Dependency Isolation
- Encapsulates Python runtime and all libraries
- Bundles NLTK resources within the image
- Prevents conflicts with host system packages

#### Portability
- Single container image works across platforms:
  - Local development environments
  - Hugging Face Spaces
  - Any Linux-based container orchestration platform

#### Simplified Deployment
- One-command deployment process
- No manual dependency installation
- Reduced deployment failure points

---

## Application Entry Point

### Primary Orchestrator: `run.py`

The entire application lifecycle is managed through a single entry point file.

#### Responsibilities

```python
# Conceptual structure of run.py

1. Initialize Flask application instance
2. Load NLP engine and preprocessing modules
3. Restore persisted BM25 index from disk
4. Launch evaluation backend as background process
5. Bind and start web server on designated port
```

#### Design Rationale

This centralized orchestration ensures:

- **Single Command Startup** — Entire system launches with `python run.py`
- **Coordinated Initialization** — All components start in correct sequence
- **Simplified Debugging** — Single point of entry for troubleshooting
- **Clean Shutdown** — Centralized cleanup on termination

---

## Container Structure

### Working Directory

The application follows a structured package layout:

```
crypto-insight-ai/          # Project root
└── crypto_sights/          # Main application package
    ├── app/                # Flask application
    └── evaluation/         # Evaluation backend
```

### Directory Layout

```
crypto-insight-ai/
├── cache/                          # Cache directory
├── crypto_sights/                  # Main application package
│   ├── app/                        # Flask application core
│   │   ├── data/                   # Data storage
│   │   │   ├── UI-UX/
│   │   │   ├── extracted_text.pickle
│   │   │   ├── extracted_textTESTING.pkl
│   │   │   ├── metrics.json
│   │   │   └── query_logs.json
│   │   ├── routes/                 # Flask route handlers
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   └── main_routes.py
│   │   ├── scripts/                # Processing and utility scripts
│   │   │   ├── __pycache__/
│   │   │   ├── crypto_scraping_model.py
│   │   │   ├── crypto.py
│   │   │   ├── keywords.py
│   │   │   ├── logger.py
│   │   │   ├── model.py
│   │   │   └── process_and_push.py
│   │   ├── static/                 # Static web assets
│   │   │   ├── assets/
│   │   │   ├── css/
│   │   │   └── js/
│   │   ├── templates/              # HTML templates
│   │   │   ├── about_us.html
│   │   │   ├── evaluation_landing.html
│   │   │   ├── evaluation.html
│   │   │   ├── faq.html
│   │   │   ├── index.html
│   │   │   ├── main_query.html
│   │   │   ├── privacy.html
│   │   │   └── terms_of_service.html
│   │   └── __init__.py
│   ├── evaluation/                 # Evaluation backend
│   │   ├── __init__.py
│   │   ├── evalbackend.py
│   │   └── evalmodel.py
│   ├── deployment.md               # Deployment documentation
│   ├── dockerfile                  # Docker container specification
│   ├── documentation.txt           # Additional documentation
│   ├── notes.tldr                  # Development notes
│   └── run.py                      # Application entry point
├── .gitattributes                  # Git attributes configuration
├── .gitignore                      # Git ignore rules
├── contributors.md                 # Contributors list
├── README.md                       # Project README
└── requirements.txt                # Python dependencies
```

### Background Process Architecture

The evaluation backend runs as an **isolated but co-located process**:

- Located in `crypto_sights/evaluation/`
- Contains `evalbackend.py` and `evalmodel.py`
- Started via `subprocess.Popen()` from `run.py`
- Shares filesystem with main application
- Stores metrics in `app/data/metrics.json` and `app/data/query_logs.json`
- Communicates through file-based or socket-based IPC
- Automatically managed by parent process lifecycle

---

## Dependency Management

### NLTK Resource Strategy

**Critical Design Decision:** All NLTK resources are downloaded during **Docker build time**, not at runtime.

#### Build-Time Download

```dockerfile
# In Dockerfile
RUN python -c "import nltk; \
    nltk.download('punkt'); \
    nltk.download('punkt_tab'); \
    nltk.download('stopwords'); \
    nltk.download('wordnet')"
```

#### Rationale

| Benefit | Explanation |
|---------|-------------|
| **Eliminates Network Dependency** | No internet required during container startup |
| **Prevents Runtime Failures** | Avoids crashes from failed downloads |
| **Reduces Cold-Start Latency** | Resources immediately available on first request |
| **Improves Reliability** | Removes external service dependency during production |

#### Required Resources

- `punkt` — Sentence tokenization
- `punkt_tab` — Enhanced tokenization tables
- `stopwords` — Common word filtering
- `wordnet` — Lemmatization and semantic analysis

---

## Resource Requirements

### Memory Profile

CryptoSights is **intentionally memory-intensive** due to its architecture:

#### Memory Consumers

1. **Large Text Corpora** — Stored in `app/data/` as pickle files
2. **In-Memory BM25 Index** — Loaded from `extracted_text.pickle` or `extracted_textTESTING.pkl`
3. **Sentence-Level Processing** — Tokenized sentences cached for analysis
4. **Multi-Process Architecture** — Flask + Evaluation backend simultaneously active
5. **Static Assets** — Templates, CSS, JS files served from `app/static/` and `app/templates/`

#### Expected Usage

- **Indexing Phase:** 1–2 GB RAM
- **Steady-State Operation:** 800 MB – 1.5 GB RAM
- **Peak Usage:** Up to 2 GB during concurrent requests

### Infrastructure Requirements

**Minimum Specifications:**
- **RAM:** 2 GB minimum, 4 GB recommended
- **CPU:** 2 cores recommended for concurrent processing
- **Storage:** 1 GB for application + indexes

**Warning:** This application is **not suitable** for low-memory environments (e.g., 512 MB containers, serverless functions with memory limits).

---

## Deployment Platform

### Why Hugging Face Spaces?

Hugging Face Spaces was selected as the deployment platform for its optimal feature set:

#### Platform Advantages

| Feature | Benefit |
|---------|---------|
| **Native Docker Support** | First-class container deployment |
| **Persistent Disk Storage** | Maintains `bm25.pkl` across restarts |
| **High-Memory CPU Instances** | Supports application memory requirements |
| **Automatic Health Monitoring** | Restarts on failure, health checks |
| **Git-Based Deployment** | Simple `git push` deployment model |
| **Zero Configuration** | Minimal setup, automatic HTTPS |

#### Ideal Use Case

Hugging Face Spaces is purpose-built for **stateful ML/NLP applications** that require:

- Persistent model/index storage
- High memory allocation
- Long-running processes
- Public accessibility

---

## Network Configuration

### Port Requirements

**Critical Configuration:** Hugging Face Docker Spaces require applications to listen on port **7860**.

#### Configuration Points

```python
# In run.py
app.run(host='0.0.0.0', port=7860)
```

```dockerfile
# In Dockerfile
EXPOSE 7860
```

#### Binding Rules

- **Host:** `0.0.0.0` (all interfaces) — Required for container accessibility
- **Port:** `7860` — Hugging Face platform requirement
- **Protocol:** HTTP (HTTPS handled by platform)

**Failure to configure correctly will result in service unreachability.**

---

## Deployment Workflow

### Step 1: Pre-Deployment Preparation

Ensure codebase is deployment-ready:

```bash
# Remove cache files
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Verify .gitignore
cat .gitignore

# Commit all changes
git add .
git commit -m "Prepare for deployment"
```

### Step 2: Local Verification (Recommended)

Test the Docker build locally before deploying:

```bash
# Build Docker image
docker build -t cryptosights .

# Run container locally
docker run -p 7860:7860 cryptosights

# Test application
curl http://localhost:7860/health
```

### Step 3: Deploy to Hugging Face Spaces

#### Initial Setup

```bash
# Clone your Hugging Face Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/crypto-insight-ai
cd crypto-insight-ai
```

#### Deploy Application

```bash
# Copy project files (from crypto_sights directory)
cp -r /path/to/crypto-insight-ai/crypto_sights/* .
cp /path/to/crypto-insight-ai/requirements.txt .
cp /path/to/crypto-insight-ai/README.md .

# Commit and push
git add .
git commit -m "Deploy CryptoSights v3.0"
git push
```

#### Automatic Build Process

Hugging Face Spaces will automatically:

1. Detect `Dockerfile` in repository
2. Build Docker image using cloud builders
3. Start container with proper port mapping
4. Expose application at `https://YOUR_USERNAME-cryptosights.hf.space`
5. Enable automatic restarts on failure

---

## Monitoring and Debugging

### Runtime Logging

Access application logs through the Hugging Face Spaces interface:

1. Navigate to your Space dashboard
2. Click **Logs** tab
3. View real-time stdout/stderr streams

### Log Management

- **Flask Logs:** Main application events, requests, errors
- **Evaluation Logs:** Background process output (suppressed to reduce noise)
- **System Logs:** Container lifecycle events

### Health Monitoring

Implement a health check endpoint:

```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'index_loaded': bm25_index is not None
    }
```

### Debugging Strategies

| Issue | Diagnostic Approach |
|-------|---------------------|
| Container won't start | Check Dockerfile syntax, verify base image |
| High memory usage | Monitor with `/health` endpoint, check index size |
| Slow responses | Profile BM25 query time, check corpus size |
| NLTK errors | Verify resources installed during build |

---

## CI/CD Pipeline

### Planned Automation (GitHub Actions)

The architecture supports automated deployment pipelines:

#### Workflow Triggers

```yaml
# .github/workflows/deploy.yml (planned)
on:
  push:
    branches:
      - main
```

#### Automated Steps

1. **Test Suite Execution** — Run unit and integration tests
2. **Docker Build** — Verify image builds successfully
3. **Deploy to Hugging Face** — Push to Space repository
4. **Health Check** — Verify deployment succeeded

#### Benefits

- **Zero-Downtime Updates** — Automated rollout process
- **Consistent Deployments** — Identical process every time
- **Reduced Human Error** — No manual deployment steps
- **Rapid Iteration** — Immediate deployment on merge

---

## Best Practices

### Development

- Always test Docker builds locally before deploying
- Use `.dockerignore` to exclude unnecessary files
- Version your BM25 index files for rollback capability

### Deployment

- Monitor memory usage in production
- Implement gradual rollout for major changes
- Maintain deployment logs for audit trail

### Maintenance

- Regularly update dependencies for security patches
- Monitor index size growth over time
- Implement index rebuilding strategy for large updates

### Optimization

**Important:** Optimize **after** deployment, not before.

- Establish baseline performance metrics first
- Profile in production environment
- Make data-driven optimization decisions

---

## System Philosophy

This deployment architecture prioritizes:

1. **Correctness** — Reliable, predictable behavior
2. **Stability** — High availability and fault tolerance
3. **Scalability** — Supports growth in data and users

The system is designed for **production use**, not experimentation. All architectural decisions favor reliability and maintainability over premature optimization.

---

## Conclusion

CryptoSights represents a production-grade NLP application deployment. By leveraging Docker containerization and Hugging Face Spaces infrastructure, the system achieves high availability, consistent performance, and simplified maintenance.

For questions or contributions, please refer to the project repository or contact the development team.

---

**Document Version:** 3.0  
**Last Updated:** January 2026  
**Maintained By:** CryptoSights Development Team