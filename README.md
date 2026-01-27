# Nexula Scan - AI/ML Security Scanner

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Nexula%20Scan-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=github)](https://github.com/marketplace/actions/nexula-scan)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The world's first comprehensive AI/ML security scanner for GitHub Actions.**

Nexula Scan provides 10 specialized security scanners to detect vulnerabilities in AI/ML projects before they reach production.

## 🚀 Features

- **10 Specialized Scanners**:
  - 🎯 Unified Scan (Intelligent orchestration)
  - 🛡️ Vulnerability Scanner (CVE detection)
  - 🤖 LLM/RAG Security (Prompt injection, jailbreaking)
  - 🧠 ML Security (Model attacks, data leakage)
  - 💉 Dataset Poisoning Detection
  - ☠️ Model Poisoning Detection
  - ⚔️ Adversarial Robustness Testing
  - 🚨 Zero-Day Threat Intelligence
  - 🐳 Container Security
  - 🔍 SAST (Static code analysis)

- **AI-Powered Analysis**: GPT-4o powered threat assessment
- **AIBOM Generation**: AI Bill of Materials for complete visibility
- **Fast & Accurate**: Scans complete in minutes
- **CI/CD Integration**: Seamless GitHub Actions workflow

## 📦 Quick Start

### Basic Usage

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Nexula Scan
        uses: nexula-labs/nexula-scan@v1
        with:
          api-key: ${{ secrets.NEXULA_API_KEY }}
```

### Advanced Usage

```yaml
name: Comprehensive Security Scan
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Nexula AI/ML Security Scan
        uses: nexula-labs/nexula-scan@v1
        with:
          api-key: ${{ secrets.NEXULA_API_KEY }}
          scan-type: 'unified'
          fail-on-critical: 'true'
          fail-on-high: 'false'
      
      - name: View Results
        if: always()
        run: |
          echo "Scan ID: ${{ steps.scan.outputs.scan-id }}"
          echo "Findings: ${{ steps.scan.outputs.findings-count }}"
          echo "View details: ${{ steps.scan.outputs.scan-url }}"
```

## 🔑 Getting Your API Key

1. Visit [nexula.one](https://nexula.one)
2. Sign up for free account
3. Generate API key from dashboard
4. Add to GitHub Secrets as `NEXULA_API_KEY`

**Free Tier**: 10 scans/month

## ⚙️ Configuration

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api-key` | Nexula API Key | Yes | - |
| `scan-type` | Type of scan to run | No | `unified` |
| `fail-on-critical` | Fail build on critical findings | No | `true` |
| `fail-on-high` | Fail build on high severity findings | No | `false` |

### Scan Types

- `unified` - Intelligent scan (recommended)
- `vulnerability` - CVE and dependency scanning
- `llm_rag` - LLM/RAG security testing
- `ml_security` - ML-specific vulnerabilities
- `dataset_poisoning` - Dataset integrity checks
- `model_poisoning` - Model backdoor detection
- `adversarial_robustness` - Adversarial attack testing
- `zero_day` - Zero-day threat detection
- `container` - Container security scanning
- `sast` - Static code analysis

### Outputs

| Output | Description |
|--------|-------------|
| `scan-id` | Unique scan identifier |
| `findings-count` | Total number of findings |
| `critical-count` | Number of critical findings |
| `high-count` | Number of high severity findings |
| `scan-url` | URL to detailed results |

## 📊 Example Results

```
╔═══════════════════════════════════════════════════════════╗
║                     SCAN RESULTS                          ║
╚═══════════════════════════════════════════════════════════╝

Total Findings: 12

  🔴 Critical: 2
  🟠 High:     3
  🟡 Medium:   5
  🟢 Low:      2

📄 View detailed results:
   https://cloud.nexula.one/scans/123
```

## 🛡️ What We Detect

### AI/ML Specific
- Prompt injection vulnerabilities
- Model backdoors and trojans
- Dataset poisoning attacks
- Adversarial example weaknesses
- Model inversion risks
- Data leakage in training
- Membership inference attacks

### Traditional Security
- CVE vulnerabilities
- Dependency issues
- Code quality problems
- Container misconfigurations
- Secret exposure
- OWASP Top 10

## 🏢 Enterprise Features

- Unlimited scans
- Priority support
- Custom integrations
- SLA guarantees
- Dedicated account manager

[Contact Sales](https://nexula.one/enterprise)

## 📚 Documentation

- [Full Documentation](https://docs.nexula.one)
- [API Reference](https://docs.nexula.one/api)
- [Security Best Practices](https://docs.nexula.one/best-practices)
- [Troubleshooting](https://docs.nexula.one/troubleshooting)

## 🤝 Support

- 📧 Email: support@nexula.one
- 💬 Discord: [Join our community](https://discord.gg/nexula)
- 🐛 Issues: [GitHub Issues](https://github.com/nexula-labs/nexula-scan/issues)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🌟 Why Nexula?

- **First AI/ML Security Platform**: Purpose-built for AI/ML projects
- **Comprehensive Coverage**: 10 specialized scanners
- **Fast & Accurate**: AI-powered analysis
- **Easy Integration**: One-line GitHub Action
- **Trusted by**: 1000+ developers worldwide

---

**Made with ❤️ by [Nexula Labs](https://nexula.one)**
