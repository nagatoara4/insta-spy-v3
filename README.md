# InstaSpy v3.0 — Professional Edition

> Professional Instagram OSINT Tool — Works on iSH arm64 iPhone

[![Version](https://img.shields.io/badge/version-3.0.0-red.svg)]()
[![Platform](https://img.shields.io/badge/platform-iSH%20arm64%20iPhone-blue.svg)]()
[![Status](https://img.shields.io/badge/status-PROFESSIONAL-purple.svg)]()

## ⚡ Real Features (Verified)

| Feature | Works on iSH? | Description |
|---------|---------------|-------------|
| Multi-Site Search | ✅ Yes | 100+ platforms username search |
| Instagram Meta | ✅ Yes | Public profile data extraction |
| Contact Extraction | ✅ Yes | Email, phone, WhatsApp, Telegram |
| Report Generation | ✅ Yes | Professional JSON export |

## ❌ Not Available (Instagram Limitations)

| Feature | Why |
|---------|-----|
| Private Profile Data | Requires authentication |
| Story Download | Requires API key |
| Follower List | Not publicly accessible |
| Activity Tracking | Requires login |

## 🚀 Quick Start

```bash
# Install
pip install requests

# Full scan
python3 src/insta_spy/cli.py full username

# Instagram only
python3 src/insta_spy/cli.py instagram username

# Multi-site search
python3 src/insta_spy/cli.py search username
```

## 📁 Architecture

```
insta-spy-v3/
├── src/insta_spy/
│   ├── cli.py                    # Command line interface
│   ├── search/
│   │   └── username_search.py    # Multi-platform search
│   ├── extract/
│   │   ├── instagram_meta.py     # Instagram data extraction
│   │   └── contact_extractor.py  # Email/phone extraction
│   └── report/
│       └── json_reporter.py      # Report generation
└── README.md
```

## ⚠️ Legal Disclaimer

For educational purposes only. Respect privacy laws.

## 📄 License

MIT

## 🙏 Built By

**worm shadow** for **He**
