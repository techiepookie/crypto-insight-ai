# 🚀 CryptoSights: Advanced Cryptocurrency Intelligence Platform

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**An intelligent NLP-powered platform for cryptocurrency news analysis, sentiment tracking, and query-based insights.**

[Features](#-key-features) • [Installation](#-quick-start) • [Architecture](#-system-architecture) • [Usage](#-usage-guide) • [API Reference](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Reference](#-api-reference)
- [Evaluation System](#-evaluation-system)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**CryptoSights** is a production-grade cryptocurrency intelligence platform that combines web scraping, natural language processing, and machine learning to deliver actionable insights from cryptocurrency news articles. The platform processes thousands of articles across major cryptocurrencies, performs advanced sentiment analysis, and provides instant, ranked answers to user queries through an intuitive web interface and RESTful API.

### Supported Cryptocurrencies

- **Bitcoin (BTC)** - Digital gold and store of value
- **Ethereum (ETH)** - Smart contract pioneer
- **Solana (SOL)** - High-performance blockchain
- **Dogecoin (DOGE)** - Community-driven memecoin
- **Hamster (HMSTR)** - Emerging cryptocurrency

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Intelligent Scraping** | Automated article collection from cryptocurrency news sources |
| **NLP Processing** | Advanced text extraction, cleaning, and preprocessing |
| **Sentiment Analysis** | Real-time sentiment tracking with polarity scoring |
| **Smart Retrieval** | BM25-powered ranked answer generation |
| **Web Interface** | Interactive query platform with visual analytics |
| **RESTful API** | Programmatic access for integration |
| **Validation Engine** | Machine learning-based answer verification |

---

## ✨ Key Features

### 🔍 Data Acquisition Pipeline

- **Automated Web Scraping**
  - Harvests up to 10 articles per cryptocurrency from trusted sources
  - Intelligent URL extraction from thenewscrypto.com
  - Built-in rate limiting and error handling
  - User-agent rotation to prevent blocking
  - Structured CSV output for audit trails

- **Robust Error Handling**
  - Automatic retry mechanisms
  - Comprehensive logging system
  - Graceful degradation on failures

### 📄 Text Processing Engine

- **Multi-Stage Extraction**
  - HTML to PDF conversion via `pdfkit`
  - Clean text extraction using `trafilatura`
  - Boilerplate removal (ads, navigation, footers)
  - Character encoding normalization

- **Advanced Preprocessing**
  - Intelligent lowercasing with acronym preservation
  - Special character handling
  - Tokenization with cryptocurrency term protection
  - Stemming and lemmatization
  - Stop word removal with domain exceptions

- **Domain-Aware Processing**
  - Cryptocurrency-specific keyword preservation
  - Technical term recognition (e.g., "DeFi", "NFT", "PoS")
  - Context-sensitive cleaning

### 💭 Sentiment Analysis System

- **Sentence-Level Analysis**
  - TextBlob-powered sentiment scoring
  - Polarity measurement (-1.0 to +1.0)
  - Subjectivity detection (0.0 to 1.0)
  - Multi-class classification (Positive, Negative, Neutral)

- **Visual Analytics**
  - Real-time sentiment distribution charts
  - Matplotlib-powered visualizations
  - Exportable graphics for reporting

### 🎯 Query Retrieval Engine

- **BM25 Algorithm Implementation**
  - Okapi BM25 ranking function
  - Tuned parameters (k1=1.5, b=0.75)
  - Efficient inverted index structure
  - Sub-second query response times

- **Rich Query Results**
  - Ranked answer ordering by relevance score
  - Source document attribution
  - Sentiment context for each result
  - Configurable result count (top-n)

### 🌐 Web Interface

- **User-Friendly Dashboard**
  - Cryptocurrency selection dropdown
  - Real-time query processing
  - Interactive result display
  - Sentiment visualization integration

- **Responsive Design**
  - Mobile-optimized layouts
  - Cross-browser compatibility
  - Modern CSS3/HTML5 standards

### 🔌 RESTful API

- **JSON-Based Communication**
  - Standardized request/response format
  - CORS-enabled for cross-origin access
  - Comprehensive error messages
  - Rate limiting ready

- **Query Logging**
  - Automatic query history tracking
  - Timestamp-based audit trail
  - Analytics-ready data format

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CryptoSights Platform                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐              ┌──────▼───────┐
        │ Data Pipeline  │              │  Web Layer   │
        └───────┬────────┘              └──────┬───────┘
                │                              │
    ┌───────────┼───────────┐          ┌───────|
    │           │           │          │       │       
┌───▼───┐   ┌──▼───┐   ┌──▼───┐   ┌──▼───┐ ┌───▼──┐
│Scraper│   │ PDF  │   │ NLP  │   │Flask │ │ REST │
│Module │   │Conver│   │Engine│   │ UI   │ │ API  │
└───┬───┘   └──┬───┘   └──┬───┘   └──┬───┘ └─┬────┘
    │          │          │          │       │
    └──────────┴──────────┴──────────┴───────┘
                        │
            ┌───────────┴───────────┐
            │                       │
        ┌───▼────┐              ┌──▼──────┐
        │  BM25  │              │Sentiment│
        │Indexing│              │Analyzer │
        └───┬────┘              └──┬──────┘
            │                      │
    ┌───────▼──────────────────────▼────────┐
    │        Query Processing Layer         │
    └───────────────────────────────────────┘
                        │
            ┌───────────┴──────────┐
            │                      │
        ┌───▼────────┐      ┌──────▼──────┐
        │ Validation │      │   Results   │
        │   Engine   │      │ Formatting  │
        └────────────┘      └─────────────┘
```

### Pipeline Flow

1. **Data Acquisition** → Web scraping → URL collection → CSV storage
2. **Content Processing** → HTML to PDF → Text extraction → Clean output
3. **NLP Processing** → Tokenization → Lemmatization → Term preservation
4. **Indexing** → BM25 index creation → Persistence → Memory optimization
5. **Query Handling** → User input → BM25 ranking → Result formatting
6. **Validation** → Semantic matching → Relevance scoring → Quality assurance

---

## 🛠️ Technology Stack

### Core Technologies

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.8+ |
| **Web Framework** | Flask 2.0+ |
| **NLP Libraries** | NLTK, TextBlob, Sentence-Transformers |
| **ML Algorithms** | BM25Okapi, Random Forest, TF-IDF |
| **Data Processing** | Pandas, NumPy |
| **Web Scraping** | BeautifulSoup4, Requests, Trafilatura |
| **Visualization** | Matplotlib, Seaborn |

### Detailed Dependencies

```python
# Web Framework & API
flask>=2.0.0
flask-cors>=3.0.10

# Web Scraping & Content Extraction
requests>=2.28.0
beautifulsoup4>=4.11.0
trafilatura>=1.4.0
pdfkit>=1.0.0

# Natural Language Processing
nltk>=3.8.0
textblob>=0.17.0
sentence-transformers>=2.2.0

# Machine Learning & Retrieval
rank-bm25>=0.2.2
scikit-learn>=1.2.0

# Data Manipulation
pandas>=1.5.0
numpy>=1.23.0

# Visualization
matplotlib>=3.6.0
seaborn>=0.12.0
```

### External Dependencies

- **wkhtmltopdf** - PDF rendering engine (required by pdfkit)
  - Installation: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- wkhtmltopdf (for PDF conversion)
- Git (for cloning the repository)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/techiepookie/crypto-insight-ai.git
cd crypto-insight-ai
```

#### 2. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Download NLTK Resources

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

Or run the following Python script:

```python
import nltk

# Download required NLTK data
resources = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'omw-1.4']
for resource in resources:
    nltk.download(resource)
```

#### 5. Install wkhtmltopdf

**Ubuntu/Debian:**
```bash
sudo apt-get install wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download installer from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

#### 6. Verify Installation

```bash
python -c "import flask, nltk, textblob, rank_bm25; print('All dependencies installed successfully!')"
```

---

## 📖 Usage Guide

### Running the Complete Pipeline

#### Option 1: Data Collection & Processing

Execute the scraping and processing pipeline:

```bash
cd crypto_sights/app/scripts
python crypto_scraping_model.py
```

**Pipeline Steps:**
1. Scrapes articles for all supported cryptocurrencies
2. Converts articles to PDF format
3. Extracts and cleans text content
4. Performs sentiment analysis
5. Builds BM25 search index
6. Saves processed data and indexes

**Output Files:**
- `{coin}_news_urls.csv` - Collected article URLs
- `{coin}_article_{n}.pdf` - Downloaded articles
- `cleaned_data.txt` - Preprocessed text corpus
- `extracted_text.pickle` - Serialized BM25 index
- Sentiment visualizations (PNG files)

#### Option 2: Start Web Application

Launch the Flask web server:

```bash
cd crypto_sights
python run.py
```

**Server Details:**
- **URL:** http://localhost:5000
- **Default Port:** 5000
- **Environment:** Development (auto-reload enabled)

### Web Interface Usage

#### Step 1: Access the Interface

Open your browser and navigate to:
```
http://localhost:5000
```

#### Step 2: Submit a Query

1. Select a cryptocurrency from the dropdown menu
2. Enter your question in the query field
   - Example: "What is driving Bitcoin's recent price increase?"
3. Click "Search" or press Enter

#### Step 3: View Results

The interface displays:
- **Overall Sentiment:** Aggregate sentiment with polarity score
- **Top Answers:** Ranked list of relevant sentences
- **Answer Details:** Each result shows:
  - Relevance score (0.0 - 1.0)
  - Source document
  - Sentiment classification
  - Full sentence context

### Command-Line Query Interface

For programmatic queries or testing:

```python
from app.scripts.model import process_query

# Execute a query
results = process_query(
    coin="bitcoin",
    query="What are analysts predicting for Bitcoin in 2025?",
    top_n=5
)

# Access results
print(f"Sentiment: {results['sentiment']}")
for idx, answer in enumerate(results['top_answers'], 1):
    print(f"{idx}. {answer}")
```

### Advanced Usage Examples

#### Custom Query with Parameters

```python
import pickle
from rank_bm25 import BM25Okapi
from app.scripts.keywords import crypto_keywords

# Load BM25 index
with open('app/data/extracted_text.pickle', 'rb') as f:
    corpus, bm25 = pickle.load(f)

# Perform custom query
query = "ethereum smart contract upgrades"
tokenized_query = query.lower().split()
scores = bm25.get_scores(tokenized_query)

# Get top results
top_indices = scores.argsort()[-10:][::-1]
results = [corpus[i] for i in top_indices]
```

#### Batch Query Processing

```python
queries = [
    "Bitcoin price prediction 2025",
    "Ethereum scaling solutions",
    "Solana network performance"
]

for query in queries:
    results = process_query("general", query, top_n=3)
    print(f"\nQuery: {query}")
    print(f"Sentiment: {results['sentiment']}")
    print(f"Top Answer: {results['top_answers'][0]}")
```

---

## 🔌 API Reference

### Base URL

```
http://localhost:5000
```

### Endpoints

#### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Verify API availability

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-15T10:30:00Z"
}
```

#### 2. Query Processing

**Endpoint:** `POST /query`

**Description:** Submit a cryptocurrency query and receive ranked answers

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "coin": "bitcoin",
  "query": "What is the latest trend in Bitcoin price?"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `coin` | string | Yes | Cryptocurrency identifier (bitcoin, ethereum, solana, dogecoin, hamster, general) |
| `query` | string | Yes | User question (max 500 characters) |

**Response (Success - 200 OK):**
```json
{
  "query": "What is the latest trend in Bitcoin price?",
  "coin": "bitcoin",
  "sentiment": "Positive (Score: 0.65)",
  "top_answers": [
    "1. Bitcoin prices surged this week due to increased institutional adoption. (Score: 0.92)",
    "2. Analysts predict Bitcoin price trends will stabilize in Q2 2025. (Score: 0.75)",
    "3. Bitcoin faced a price dip amid regulatory concerns. (Score: 0.68)"
  ],
  "metadata": {
    "processing_time_ms": 145,
    "total_documents_searched": 1247,
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```

**Response (Error - 400 Bad Request):**
```json
{
  "error": "Invalid coin parameter",
  "message": "Coin must be one of: bitcoin, ethereum, solana, dogecoin, hamster, general",
  "status": 400
}
```

**Response (Error - 500 Internal Server Error):**
```json
{
  "error": "Query processing failed",
  "message": "BM25 index not loaded",
  "status": 500
}
```

### cURL Examples

#### Basic Query
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "coin": "ethereum",
    "query": "What are the latest Ethereum upgrades?"
  }'
```

#### General Crypto Query
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{
    "coin": "general",
    "query": "What is DeFi?"
  }'
```

### Python SDK Example

```python
import requests
import json

class CryptoSightsClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def query(self, coin, question):
        """Submit a query to CryptoSights API"""
        endpoint = f"{self.base_url}/query"
        payload = {"coin": coin, "query": question}
        
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()

# Usage
client = CryptoSightsClient()
results = client.query("bitcoin", "What drives Bitcoin volatility?")
print(results['sentiment'])
```

---

## 🎓 Evaluation System

### Overview

The **Validation Engine** ensures answer quality through machine learning-based relevance scoring and semantic matching.

### Architecture

```
┌─────────────────────────────────────────────┐
│         Evaluation System Pipeline          │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    ┌───▼────────┐      ┌──────▼──────┐
    │   Input    │      │  Validation │
    │  Checker   │      │   Rules     │
    └───┬────────┘      └──────┬──────┘
        │                      │
        └──────────┬───────────┘
                   │
           ┌───────▼────────┐
           │   Keyword      │
           │   Matching     │
           └───────┬────────┘
                   │
           ┌───────▼────────┐
           │   Semantic     │
           │   Similarity   │
           │  (BERT/SBERT)  │
           └───────┬────────┘
                   │
           ┌───────▼────────┐
           │  TF-IDF Vector │
           │  Representation│
           └───────┬────────┘
                   │
           ┌───────▼────────┐
           │  Random Forest │
           │   Classifier   │
           └───────┬────────┘
                   │
           ┌───────▼────────┐
           │ Valid/Invalid  │
           │ Classification │
           └────────────────┘
```

### Core Components

#### 1. Data Input & Validation

**Function:** `load_data(file_path)` / `fetch_api(url)`

**Input Format:**
```json
{
  "coin": "bitcoin",
  "query": "What is Bitcoin halving?",
  "answers": [
    "Bitcoin halving reduces mining rewards by 50%.",
    "The next halving is expected in 2028.",
    "Halving events historically impact Bitcoin price."
  ]
}
```

**Validation Checks:**
- Non-empty coin, query, and answers
- Valid cryptocurrency identifier
- Answer array contains at least one entry

#### 2. Entry Validation

**Function:** `is_valid_entry(entry)`

**Validation Strategy:**

```python
def is_valid_entry(entry):
    """
    Multi-stage validation pipeline:
    1. Special case handling (e.g., "general crypto")
    2. Null/empty field detection
    3. Keyword matching (coin terms in query/answers)
    4. Semantic similarity (BERT embeddings)
    """
    # Stage 1: Special cases
    if entry['coin'].lower() == 'general crypto':
        return True
    
    # Stage 2: Basic validation
    if not entry['query'] or not entry['answers']:
        return False
    
    # Stage 3: Keyword matching
    if has_keyword_match(entry):
        return True
    
    # Stage 4: Semantic matching (threshold: 0.5)
    similarity = compute_semantic_similarity(entry)
    return similarity >= 0.5
```

**Semantic Similarity:**
- Uses `sentence-transformers` library
- Model: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- Cosine similarity threshold: **0.5**
- Compares coin context with answer embeddings

#### 3. Feature Engineering

**TF-IDF Vectorization:**

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Concatenate text fields
combined_text = entry['coin'] + " " + entry['query'] + " " + " ".join(entry['answers'])

# Create TF-IDF features
vectorizer = TfidfVectorizer(
    max_features=500,
    ngram_range=(1, 2),
    stop_words='english'
)
features = vectorizer.fit_transform([combined_text])
```

**Label Encoding:**
```python
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
status_encoded = encoder.fit_transform(status_labels)  # valid → 1, invalid → 0
```

#### 4. Machine Learning Classifier

**Algorithm:** Random Forest Classifier

**Configuration:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Hyperparameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Grid search with cross-validation
clf = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1'
)
```

**Performance Metrics:**
- Precision, Recall, F1-Score
- Confusion Matrix
- Classification Report

#### 5. Output Format

**CSV Structure:**
```csv
coin,query,status,formatted_answers,tfidf_feature_1,...,tfidf_feature_n,status_encoded
bitcoin,"What is halving?",valid,"Bitcoin halving reduces...",0.23,...,0.15,1
ethereum,"Latest upgrades",valid,"Ethereum 2.0 introduces...",0.31,...,0.08,1
dogecoin,"Investment strategy",invalid,"Not enough relevant info",0.12,...,0.04,0
```

### Integration with Backend

**Flask Route (Planned):**

```python
@app.route('/validate', methods=['POST'])
def validate_answer():
    """Real-time answer validation endpoint"""
    data = request.json
    
    # Load pre-trained model
    with open('models/validator.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Validate entry
    is_valid = is_valid_entry(data)
    confidence = model.predict_proba([data])[0][1]
    
    return jsonify({
        'valid': is_valid,
        'confidence': float(confidence),
        'threshold': 0.5
    })
```

### Usage Example

```python
from evaluation.evalmodel import is_valid_entry, vectorize_data

# Sample entry
entry = {
    'coin': 'bitcoin',
    'query': 'What factors influence Bitcoin price?',
    'answers': [
        'Supply and demand dynamics affect Bitcoin price.',
        'Regulatory news impacts market sentiment.',
        'Institutional adoption drives price increases.'
    ]
}

# Validate
is_valid = is_valid_entry(entry)
print(f"Entry valid: {is_valid}")  # True

# Vectorize for ML model
features, labels = vectorize_data([entry])
```

---

## 📁 Project Structure

```
crypto-insight-ai/
├── cache/                              # Temporary cache storage
├── crypto_sights/                      # Main application package
│   ├── app/                            # Flask application core
│   │   ├── data/                       # Data storage
│   │   │   ├── UI-UX/                  # UI/UX assets
│   │   │   ├── extracted_text.pickle   # BM25 index (production)
│   │   │   ├── extracted_textTESTING.pkl # BM25 index (testing)
│   │   │   ├── metrics.json            # Performance metrics
│   │   │   └── query_logs.json         # Query history
│   │   ├── routes/                     # Flask route handlers
│   │   │   ├── __init__.py
│   │   │   └── main_routes.py          # API endpoints
│   │   ├── scripts/                    # Processing scripts
│   │   │   ├── crypto_scraping_model.py # Main scraping pipeline
│   │   │   ├── crypto.py               # Crypto utilities
│   │   │   ├── keywords.py             # Domain keywords
│   │   │   ├── logger.py               # Logging utilities
│   │   │   ├── model.py                # NLP model
│   │   │   └── process_and_push.py     # Data processing
│   │   ├── static/                     # Static web assets
│   │   │   ├── assets/                 # Images, icons
│   │   │   ├── css/                    # Stylesheets
│   │   │   │   └── style.css
│   │   │   └── js/                     # JavaScript files
│   │   │       └── main.js
│   │   ├── templates/                  # HTML templates
│   │   │   ├── about_us.html
│   │   │   ├── evaluation_landing.html
│   │   │   ├── evaluation.html
│   │   │   ├── faq.html
│   │   │   ├── index.html              # Main interface
│   │   │   ├── main_query.html
│   │   │   ├── privacy.html
│   │   │   └── terms_of_service.html
│   │   └── __init__.py                 # App initialization
│   ├── evaluation/                     # Validation engine
│   │   ├── __init__.py
│   │   ├── evalbackend.py              # Validation backend
│   │   └── evalmodel.py                # ML validation model
│   ├── deployment.md                   # Deployment guide
│   ├── dockerfile                      # Docker configuration
│   ├── documentation.txt               # Additional docs
│   ├── notes.tldr                      # Development notes
│   └── run.py                          # Application entry point
├── .gitattributes                      # Git attributes
├── .gitignore                          # Git ignore rules
├── contributors.md                     # Contributors list
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
└── LICENSE                             # License information
```

### Key Directories Explained

#### `/app/data/`
**Purpose:** Persistent data storage for indexes, logs, and metrics

- `extracted_text.pickle` - Production BM25 index (optimized)
- `extracted_textTESTING.pkl` - Development/testing index
- `metrics.json` - System performance metrics
- `query_logs.json` - Historical query data for analytics

#### `/app/scripts/`
**Purpose:** Core processing logic and utilities

- `crypto_scraping_model.py` - Main data acquisition pipeline
- `model.py` - NLP processing and query handling
- `keywords.py` - Cryptocurrency-specific term dictionary
- `logger.py` - Query logging and audit trails

#### `/app/static/` & `/app/templates/`
**Purpose:** Web interface assets

- Static files served directly by Flask
- Templates rendered with Jinja2 engine
- Responsive design with modern CSS

#### `/evaluation/`
**Purpose:** Answer validation and quality assurance

- ML-based relevance scoring
- Semantic similarity computation
- Classification model training

---

## 💻 Development

### Setting Up Development Environment

#### 1. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

**Development Dependencies:**
```
# Testing
pytest>=7.2.0
pytest-cov>=4.0.0
pytest-flask>=1.2.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
pylint>=2.16.0
mypy>=1.0.0

# Documentation
sphinx>=5.3.0
sphinx-rtd-theme>=1.2.0
```

#### 2. Configure Pre-Commit Hooks

```bash
pip install pre-commit
pre-commit install
```

**`.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=crypto_sights --cov-report=html

# Run specific test file
pytest tests/test_model.py

# Run with verbose output
pytest -v
```

### Code Quality Checks

```bash
# Format code with Black
black crypto_sights/

# Lint with Flake8
flake8 crypto_sights/ --max-line-length=100

# Type checking with MyPy
mypy crypto_sights/

# Comprehensive linting
pylint crypto_sights/
```

### Project Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following PEP 8 style guide
   - Add docstrings to functions and classes
   - Update tests as needed

3. **Test Locally**
   ```bash
   pytest
   black crypto_sights/
   flake8 crypto_sights/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**
```
feat: add Solana sentiment analysis
fix: resolve BM25 index loading error
docs: update API reference with new endpoints
refactor: optimize text preprocessing pipeline
```

---

## 🚢 Deployment

### Docker Deployment

The application is containerized for consistent deployment across environments.

#### Build Docker Image

```bash
cd crypto_sights
docker build -t cryptosights:latest .
```

#### Run Container Locally

```bash
docker run -d \
  -p 7860:7860 \
  --name cryptosights \
  -v $(pwd)/app/data:/app/app/data \
  cryptosights:latest
```

#### Docker Compose (Recommended)

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  cryptosights:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./app/data:/app/app/data
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Start Services:**
```bash
docker-compose up -d
```

### Hugging Face Spaces Deployment

#### Prerequisites
1. Create a Hugging Face account
2. Create a new Space (Docker type)
3. Clone your Space repository

#### Deployment Steps

```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/cryptosights
cd cryptosights

# Copy application files
cp -r /path/to/crypto-insight-ai/crypto_sights/* .
cp /path/to/crypto-insight-ai/requirements.txt .

# Commit and push
git add .
git commit -m "Deploy CryptoSights v1.0"
git push
```

#### Hugging Face Configuration

Create `README.md` in Space root:
```yaml
---
title: CryptoSights
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---
```

**Note:** Hugging Face Spaces automatically builds and deploys Docker containers.

### Environment Variables

Create `.env` file for production configuration:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here

# Application Settings
MAX_QUERY_LENGTH=500
DEFAULT_TOP_N=5
ENABLE_LOGGING=true

# Data Paths
DATA_DIR=/app/app/data
INDEX_PATH=/app/app/data/extracted_text.pickle
LOG_PATH=/app/app/data/query_logs.json
```

### Monitoring & Maintenance

#### Health Monitoring

```bash
# Check application health
curl http://localhost:7860/health

# Monitor logs
docker logs -f cryptosights

# Check resource usage
docker stats cryptosights
```

#### Performance Optimization

1. **Index Optimization**
   - Rebuild BM25 index periodically
   - Remove outdated documents
   - Compress pickle files

2. **Caching Strategy**
   - Implement Redis for query caching
   - Cache frequent queries for 24 hours
   - Use ETags for static assets

3. **Load Balancing**
   - Deploy multiple instances behind load balancer
   - Use nginx for reverse proxy
   - Implement request queuing

---

## 🤝 Contributing

We welcome contributions from the community! Whether it's bug fixes, feature additions, documentation improvements, or testing, your help is appreciated.

### How to Contribute

#### 1. Fork the Repository

Click the "Fork" button on the [GitHub repository](https://github.com/techiepookie/crypto-insight-ai)

#### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/crypto-insight-ai.git
cd crypto-insight-ai
```

#### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

#### 4. Make Your Changes

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

#### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: description of your changes"
```

#### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

#### 7. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Submit for review

### Contribution Guidelines

#### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters

**Example:**
```python
def extract_sentiment(text: str) -> dict:
    """
    Extract sentiment polarity and subjectivity from text.
    
    Args:
        text (str): Input text for sentiment analysis
        
    Returns:
        dict: Dictionary with 'polarity', 'subjectivity', and 'label' keys
        
    Raises:
        ValueError: If text is empty or None
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    blob = TextBlob(text)
    return {
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity,
        'label': categorize_sentiment(blob.sentiment.polarity)
    }
```

#### Testing Requirements

- Write unit tests for new functions
- Maintain >80% code coverage
- Include integration tests for API endpoints
- Test edge cases and error handling

**Example Test:**
```python
def test_extract_sentiment_positive():
    """Test sentiment extraction for positive text"""
    text = "Bitcoin is performing exceptionally well today!"
    result = extract_sentiment(text)
    
    assert result['polarity'] > 0
    assert result['label'] == 'Positive'
    assert 0 <= result['subjectivity'] <= 1
```

#### Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Include docstrings with type hints
- Update API documentation for endpoint changes


### Code Review Process

1. **Automated Checks** - CI/CD runs tests and linting
2. **Maintainer Review** - Core team reviews code quality
3. **Discussion** - Address feedback and make changes
4. **Approval** - Minimum 1 approving review required
5. **Merge** - Squash and merge to main branch

### Recognition

Contributors are recognized in:
- `contributors.md` file
- GitHub contributors page
- Release notes for significant contributions

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Copyright (c) 2025 CryptoSights Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 📞 Contact & Support

### Get Help

- **Documentation:** [Read the docs](https://cryptosights.gitbook.io/cryptosights-docs)
- **Issues:** [Report bugs or request features](https://github.com/techiepookie/crypto-insight-ai/issues)

### Stay Connected

- **GitHub:** [@techiepookie](https://github.com/techiepookie)
- **Project Repository:** [crypto-insight-ai](https://github.com/techiepookie/crypto-insight-ai)

### Support the Project

If you find CryptoSights useful, consider:

- ⭐ **Star the repository** on GitHub
- 🐛 **Report bugs** to help improve the platform
- 💡 **Suggest features** for future development
- 🤝 **Contribute code** or documentation
- 📢 **Share the project** with others

---

## 🙏 Acknowledgments

### Core Team

Special thanks to all contributors who have helped build CryptoSights:

- **Lead Developer:** Harshal Chaudhari & Nikhil Kumar Obhawani
- **Contributors:** See [contributors.md](contributors.md) for full list

### Technologies & Libraries

We're grateful to the open-source community for these excellent tools:

- **Flask** - Web framework foundation
- **NLTK** - Natural language processing
- **TextBlob** - Sentiment analysis
- **BeautifulSoup** - Web scraping
- **scikit-learn** - Machine learning utilities
- **Hugging Face** - Deployment infrastructure

### Data Sources

- **TheNewsCrypto** - Cryptocurrency news aggregation
- **Community Contributors** - Test data and feedback


---


<div align="center">

**Built with ❤️ by the CryptoSights Team**

[⬆ Back to Top](#-cryptosights-advanced-cryptocurrency-intelligence-platform)

</div>