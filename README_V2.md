# ReconAI v2.0 - OSINT Intelligence Platform

**Domain & Person Intelligence Suite**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🚀 What's New in v2.0

### Person Intelligence Module

ReconAI now supports comprehensive **person background checks** in addition to domain reconnaissance:

- **Criminal Records Search** - Federal, state, and county criminal databases
- **Court Records Search** - PACER, state courts, municipal courts
- **Professional Licenses** - Medical, legal, nursing, and other professional boards
- **Social Media Intelligence** - Facebook, Twitter, LinkedIn, Instagram, TikTok
- **Public Records** - Voter registration, property ownership, business registrations
- **All 50 US States** - State-specific sources and databases

---

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Domain Intelligence](#domain-intelligence)
  - [Person Intelligence](#person-intelligence)
- [API Documentation](#api-documentation)
- [Legal Notice](#legal-notice)
- [Data Sources](#data-sources)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Domain Intelligence (v1.0)

- **Domain Intelligence** - DNS, WHOIS, subdomains, IP addresses
- **Web Intelligence** - Technologies, security headers, SSL/TLS
- **Network Intelligence** - Port scanning, service detection, banners
- **Social Intelligence** - GitHub, social profiles, public mentions
- **Threat Intelligence** - Breach checks, reputation, vulnerabilities

### Person Intelligence (v2.0) 🆕

- **Criminal Records** - NSOPW, Federal BOP, state databases
- **Court Records** - Federal, state, county, municipal
- **Professional Info** - LinkedIn, licenses, certifications
- **Social Media** - Comprehensive social profile search
- **Public Records** - Voter registration, property, businesses
- **State-Specific** - Tailored searches for all 50 states

### AI-Powered Analysis

- **Executive Summaries** - Natural language intelligence reports
- **Risk Scoring** - 0-100 scale risk assessment
- **Pattern Recognition** - AI correlates findings across sources
- **Recommendations** - Actionable security recommendations

---

## 🔧 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- OpenAI API key (for AI analysis)

### Install Dependencies

```bash
git clone https://github.com/CoryLawsonxMortgageAI/ReconAI.git
cd ReconAI
pip install -r requirements.txt
```

### Set Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

---

## 🚀 Quick Start

### Start the Application

```bash
python3 app.py
```

The application will be available at `http://localhost:8000`

### Web Interface

1. Open browser to `http://localhost:8000`
2. Select target type: **Domain** or **Person**
3. Enter target information
4. Click "Start Reconnaissance"
5. View comprehensive results and AI analysis

---

## 📖 Usage

### Domain Intelligence

**Web Interface:**
1. Select "Domain / IP Address" from Target Type
2. Enter domain (e.g., `example.com`)
3. Choose scan type (Full, Quick, or Custom)
4. Click "Start Reconnaissance"

**API:**
```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "target_type": "domain",
    "scan_type": "full",
    "modules": ["domain", "web", "network", "social", "threat"]
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/scan",
    json={
        "target": "example.com",
        "target_type": "domain",
        "scan_type": "full"
    }
)

results = response.json()
print(results["analysis"]["summary"])
```

### Person Intelligence 🆕

**Web Interface:**
1. Select "Person / Individual" from Target Type
2. Enter full name (e.g., `John Smith`)
3. Optionally select state (e.g., `California`)
4. Optionally enter date of birth
5. Click "Start Reconnaissance"

**API:**
```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "target": "John Smith",
    "target_type": "person",
    "state": "CA",
    "dob": "1980-01-15",
    "scan_type": "full"
  }'
```

**Python:**
```python
import asyncio
from modules.person_intel import PersonIntelligence

async def scan_person():
    person_intel = PersonIntelligence()
    
    results = await person_intel.scan(
        person_name="John Smith",
        state="CA",
        dob="1980-01-15"
    )
    
    print(results)

asyncio.run(scan_person())
```

---

## 📚 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/health` | GET | Health check |
| `/api/scan` | POST | Start reconnaissance scan |
| `/api/scan/{scan_id}` | GET | Get scan results |
| `/api/scans` | GET | List recent scans |
| `/api/stats` | GET | Platform statistics |

### Request Schema

```json
{
  "target": "string",
  "target_type": "domain | person",
  "scan_type": "full | quick | custom",
  "state": "string (optional, for person)",
  "dob": "string (optional, for person)",
  "modules": ["array", "of", "modules"]
}
```

### Response Schema

```json
{
  "scan_id": "uuid",
  "target": "string",
  "target_type": "domain | person",
  "status": "completed | failed",
  "results": {
    "domain": {...},
    "web": {...},
    "network": {...},
    "social": {...},
    "threat": {...},
    "person": {...}
  },
  "analysis": {
    "summary": "string",
    "risk_score": 0-100,
    "recommendations": ["array"]
  },
  "timestamp": "ISO 8601"
}
```

---

## ⚖️ Legal Notice

### Authorized Use Only

This tool is designed for **authorized security testing and investigations only**. Unauthorized use may violate:

- Computer Fraud and Abuse Act (CFAA)
- Fair Credit Reporting Act (FCRA)
- State privacy laws (CCPA, VCDPA, etc.)
- Driver's Privacy Protection Act (DPPA)

### Permitted Uses

✅ Pre-employment background checks (with consent)  
✅ Tenant screening (with consent)  
✅ Due diligence investigations  
✅ Legal proceedings and discovery  
✅ Fraud investigations  
✅ Missing persons investigations  
✅ Genealogical research  
✅ Academic research  

### Prohibited Uses

❌ Stalking or harassment  
❌ Identity theft  
❌ Discrimination  
❌ Unauthorized credit decisions  
❌ Invasion of privacy  
❌ Doxxing or public shaming  

### Compliance

**FCRA Compliance:**
- Obtain written consent for employment/tenant screening
- Provide required disclosures
- Follow adverse action procedures

**Privacy Laws:**
- Respect state privacy regulations
- Secure collected data
- Delete data when no longer needed

**See [PERSON_INTELLIGENCE.md](PERSON_INTELLIGENCE.md) for detailed legal guidelines.**

---

## 🗂️ Data Sources

### Criminal Records

- National Sex Offender Public Website (NSOPW)
- Federal Bureau of Prisons (BOP)
- State criminal databases (all 50 states)
- County sheriff offices
- State departments of corrections

### Court Records

- PACER (Federal courts)
- State court systems
- County clerk of court offices
- Municipal courts

### Professional Information

- LinkedIn
- State medical boards
- State bar associations
- Nursing boards
- Professional licensing boards

### Public Records

- Voter registration databases
- County property records
- Secretary of State business divisions
- SEC EDGAR database
- Vital records offices

---

## 🏗️ Architecture

```
ReconAI/
├── app.py                      # Main application (v2.0)
├── modules/
│   ├── domain_intel.py         # Domain intelligence
│   ├── web_intel.py            # Web intelligence
│   ├── network_intel.py        # Network intelligence
│   ├── social_intel.py         # Social intelligence
│   ├── threat_intel.py         # Threat intelligence
│   ├── person_intel.py         # Person intelligence 🆕
│   ├── llm_analyzer.py         # AI analysis
│   └── database.py             # Data persistence
├── templates/
│   └── index.html              # Web interface
├── static/
│   ├── css/style.css           # Styling
│   └── js/app.js               # Frontend logic
├── data/                       # SQLite database
├── logs/                       # Application logs
└── README.md                   # This file
```

---

## 🧪 Testing

### Run Tests

```bash
# Test domain intelligence
python3 test_scan.py

# Test person intelligence
python3 test_person_scan.py
```

### Example Test Output

```
============================================================
Testing: John Smith
State: CA
============================================================
{
  "target": "John Smith",
  "state": "CA",
  "criminal_records": [
    {
      "source": "NSOPW",
      "status": "No records found"
    },
    {
      "source": "Federal Bureau of Prisons",
      "status": "Search completed"
    }
  ],
  "court_cases": [...],
  "professional_info": {...},
  "social_media": {...},
  "public_records": {...}
}
```

---

## 📊 Statistics

| Metric | Value |
|:-------|:------|
| Lines of Code | 2,000+ |
| Modules | 7 |
| Data Sources | 50+ |
| States Supported | 50 |
| Record Types | 10+ |

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Areas for Contribution:**
- Additional data source integrations
- Enhanced AI analysis
- UI/UX improvements
- Documentation
- Test coverage

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub:** https://github.com/CoryLawsonxMortgageAI/ReconAI
- **Documentation:** [PERSON_INTELLIGENCE.md](PERSON_INTELLIGENCE.md)
- **Issues:** https://github.com/CoryLawsonxMortgageAI/ReconAI/issues

---

## ⚠️ Disclaimer

This tool is provided for authorized investigative and research purposes only. Users are responsible for ensuring their use complies with all applicable federal, state, and local laws. The developers assume no liability for misuse or unauthorized use of this tool.

**Always:**
- Obtain proper authorization
- Follow legal requirements
- Respect privacy rights
- Use data responsibly
- Verify critical information

---

## 📞 Support

For questions, issues, or feature requests:

- Open an issue on GitHub
- Review the documentation
- Check existing issues for solutions

---

**Version:** 2.0.0  
**Last Updated:** October 23, 2025  
**Status:** Production Ready ✅

