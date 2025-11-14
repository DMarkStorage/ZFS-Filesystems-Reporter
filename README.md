# 📊 ZFS Filesystems Reporter

> **Automate Oracle ZFS Storage audits with enterprise-grade security—export filesystem data to CSV/JSON in seconds, not hours.**

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/yourusername/ZFS-Filesystems-Reporter)](https://github.com/yourusername/ZFS-Filesystems-Reporter)
[![Code Size](https://img.shields.io/github/languages/code-size/yourusername/ZFS-Filesystems-Reporter)](https://github.com/yourusername/ZFS-Filesystems-Reporter)

---

## 📑 Table of Contents

- [📊 ZFS Filesystems Reporter](#-zfs-filesystems-reporter)
  - [📑 Table of Contents](#-table-of-contents)
  - [🚀 Project Overview](#-project-overview)
    - [Who is this for?](#who-is-this-for)
  - [✨ Key Features](#-key-features)
  - [🎥 See It In Action](#-see-it-in-action)
    - [Terminal Output Example](#terminal-output-example)
    - [Sample CSV Output](#sample-csv-output)
  - [🛠️ Getting Started](#️-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Option 1: Clone from GitHub (Recommended)](#option-1-clone-from-github-recommended)
      - [Option 2: Direct Download](#option-2-direct-download)
  - [⚙️ Usage Examples](#️-usage-examples)
    - [Quick Start](#quick-start)
    - [Advanced Usage](#advanced-usage)
      - [Preview Data Before Export](#preview-data-before-export)
    - [Command-Line Reference](#command-line-reference)
  - [📚 Documentation \& Architecture](#-documentation--architecture)
    - [High-Level Architecture](#high-level-architecture)
    - [Core Functions](#core-functions)
    - [API Endpoint Details](#api-endpoint-details)
  - [🤝 Contributing](#-contributing)
    - [How to Contribute](#how-to-contribute)
    - [Contribution Guidelines](#contribution-guidelines)
  - [🔒 Security Best Practices](#-security-best-practices)
    - [✅ What We Do](#-what-we-do)
    - [🔧 Vault Configuration](#-vault-configuration)
    - [⚠️ Security Considerations](#️-security-considerations)
  - [� License](#-license)
  - [🙏 Acknowledgements](#-acknowledgements)
  - [📬 Contact \& Support](#-contact--support)
    - [Connect with the Maintainer](#connect-with-the-maintainer)

---

## 🚀 Project Overview

**ZFS Filesystems Reporter** is a production-ready Python automation tool designed for enterprise storage administrators managing Oracle ZFS Storage Appliances. It eliminates manual data collection by connecting directly to ZFS appliances via their REST API, extracting comprehensive filesystem metadata, and exporting clean, structured reports in both CSV and JSON formats.

**Why it matters:** Storage teams waste hours manually documenting configurations for audits, capacity planning, and compliance reviews. This tool reduces that process to a single command while maintaining enterprise-grade security through HashiCorp Vault integration—no hardcoded credentials, no security risks.

### Who is this for?

- **🔧 Storage Administrators** needing quick filesystem inventories
- **📊 Data Engineers** integrating storage metrics into dashboards
- **✅ Compliance Officers** requiring standardized audit reports
- **🤖 DevOps Teams** automating infrastructure monitoring

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **Secure by Default** | HashiCorp Vault integration—credentials never touch code or logs |
| 📤 **Dual Export Formats** | CSV for Excel analysis, JSON for API/automation workflows |
| 👀 **CLI Preview Mode** | Verify data instantly with formatted terminal tables |
| ⚡ **Production-Ready** | Robust error handling, graceful failures, clear logging |
| 🎯 **Focused Data Extraction** | Pulls only what matters: pools, shares, protocols, capacity |
| 🔄 **RESTful Integration** | Clean API client pattern—easily adaptable to other endpoints |

---

## 🎥 See It In Action

### Terminal Output Example

```bash
$ python Filesystems_Reporter.py -s zfs-prod-01 -fl storage_audit -v 5

Fetching data from zfs-prod-01...
Retrieved 127 filesystems

=== Filesystem Report (showing first 5 of 127 rows) ===
╒══════════════════════╤═══════════════╤════════════════╤════════════════════╕
│ Name                 │ Pool          │ ShareSMB       │ Space Data (GB)    │
╞══════════════════════╪═══════════════╪════════════════╪════════════════════╡
│ prod_data_01         │ pool_primary  │ on             │ 2,847.3            │
├──────────────────────┼───────────────┼────────────────┼────────────────────┤
│ backup_archive       │ pool_backup   │ off            │ 5,120.8            │
├──────────────────────┼───────────────┼────────────────┼────────────────────┤
│ dev_environment      │ pool_primary  │ on             │ 891.2              │
╘══════════════════════╧═══════════════╧════════════════╧════════════════════╛

✅ CSV and JSON files created successfully!
   - storage_audit.csv
   - storage_audit.json
```

### Sample CSV Output

```csv
Name,Pool,ShareSMB,Sharesmb Name,Sharenfs,Shareftp,Space data,space_total
prod_data_01,pool_primary,on,ProdData,off,off,2847300000000,4000000000000
backup_archive,pool_backup,off,,off,off,5120800000000,8000000000000
```


---

## 🛠️ Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.6+ | Developed and tested on Python 3.8+ |
| **pip** | Latest | Python package installer |
| **HashiCorp Vault** | Any | Access to a Vault instance with ZFS credentials |
| **Network Access** | Port 215 | To your Oracle ZFS Storage Appliance |

**Optional but Recommended:**
- `virtualenv` or `venv` for isolated Python environments
- `git` for version control

---

### Installation

#### Option 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/DMarkStorage/ZFS-Filesystems-Reporter.git

# Navigate to the project directory
cd ZFS-Filesystems-Reporter

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Direct Download

```bash
# Download the script directly
wget https://raw.githubusercontent.com/DMarkStorage/ZFS-Filesystems-Reporter.git

# Install dependencies manually
pip install -r requirements.txt
```


---

## ⚙️ Usage Examples

### Quick Start

Run your first report in under 30 seconds:

```bash
# Basic usage: Generate CSV and JSON reports
python Filesystems_Reporter.py -s your-zfs-hostname -fl my_storage_report

# Example with real hostname
python Filesystems_Reporter.py -s zfs-prod-01.company.com -fl prod_audit_2024
```

**What happens:**
1. ✅ Script connects to `zfs-prod-01.company.com` on port 215
2. ✅ Retrieves credentials securely from Vault
3. ✅ Fetches all filesystem data via REST API
4. ✅ Generates two files:
   - `prod_audit_2024.csv`
   - `prod_audit_2024.json`

---

### Advanced Usage

#### Preview Data Before Export

```bash
# View the first 10 rows in your terminal
python Filesystems_Reporter.py -s zfs-prod-01 -fl report -v 10

# Or use the long-form flag
python Filesystems_Reporter.py -s zfs-prod-01 -fl report --view 15
```


---

### Command-Line Reference

```
Usage:
    Filesystems_Reporter.py -s <STORAGE> -fl <FILENAME> [-v <NUM> | --view <NUM>]
    Filesystems_Reporter.py --version
    Filesystems_Reporter.py -h | --help

Options:
    -h --help            Show this help message and exit
    -s <STORAGE>         ZFS appliance hostname or IP address
    -fl <FILENAME>       Base filename for output (without extension)
    -v <NUM>             Preview the first NUM rows in terminal
    --view <NUM>         Same as -v (alternative syntax)
    --version            Display version information

Examples:
    Filesystems_Reporter.py -s zfs-01.local -fl weekly_report
    Filesystems_Reporter.py -s 192.168.1.100 -fl audit_q4 -v 20
```

---

## 📚 Documentation & Architecture

### High-Level Architecture

```
┌─────────────────────┐
│   User CLI Command  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐      ┌──────────────────┐
│  Vault Integration  │─────▶│ Credential Fetch │
│  (get_headers())    │      │  (Secure Secrets)│
└──────────┬──────────┘      └──────────────────┘
           │
           ▼
┌─────────────────────┐
│   REST API Client   │
│  (get_projects())   │─────▶ ZFS Appliance
└──────────┬──────────┘       (Port 215)
           │
           ▼
┌─────────────────────┐
│  Data Extraction &  │
│   Transformation    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐      ┌──────────────────┐
│   Export Engine     │─────▶│  CSV + JSON      │
│  (write_data())     │      │  Output Files    │
└─────────────────────┘      └──────────────────┘
```

### Core Functions

| Function | Purpose | Key Logic |
|----------|---------|-----------|
| `get_headers()` | Retrieves credentials from Vault | Validates secret fetch; raises exception on failure |
| `get_projects(storage)` | Queries ZFS REST API | Uses `requests.get()` with error handling via `raise_for_status()` |
| `write_data(rows, filename)` | Exports to CSV/JSON | Uses pandas DataFrame for consistent formatting |
| `view_rows(rows, count)` | CLI preview | Leverages `tabulate` for formatted table output |
| `main(cli_args)` | Entry point | Orchestrates workflow; handles CLI argument parsing |

### API Endpoint Details

**Base URL Format:**
```
https://<STORAGE_HOSTNAME>:215/api/storage/v1/filesystems
```

**Authentication Headers:**
```json
{
  "Content-Type": "application/json",
  "X-Auth-User": "<vault_username>",
  "X-Auth-Key": "<vault_password>"
}
```

**Response Schema (Simplified):**
```json
{
  "filesystems": [
    {
      "name": "prod_data_01",
      "pool": "pool_primary",
      "sharesmb": "on",
      "sharesmb_name": "ProdData",
      "sharenfs": "off",
      "shareftp": "off",
      "space_data": 2847300000000,
      "space_total": 4000000000000
    }
  ]
}
```

---


---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ZFS-Filesystems-Reporter.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
4. **Make your changes** and commit:
   ```bash
   git commit -m "Add amazing new feature that does X"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-new-feature
   ```
6. **Open a Pull Request** on the main repository



### Contribution Guidelines

- ✅ Follow PEP 8 style guidelines
- ✅ Add docstrings to all functions
- ✅ Include unit tests for new features
- ✅ Update documentation as needed
- ✅ Keep commits atomic and well-described



---

## 🔒 Security Best Practices

This tool implements enterprise security standards:

### ✅ What We Do

- **No Hardcoded Credentials**: All secrets retrieved from HashiCorp Vault at runtime
- **Minimal Permissions**: Uses read-only API credentials
- **No Logging of Secrets**: Credentials never written to logs or stdout
- **Graceful Error Handling**: Fails securely without exposing sensitive data

### 🔧 Vault Configuration

Store credentials in Vault using this structure:

```bash
# Write secrets to Vault
vault kv put it-storage/KVv1/oracle/ZFS/zapi_ro_user \
  username="readonly_api_user" \
  password="your_secure_password"

# Verify storage
vault kv get it-storage/KVv1/oracle/ZFS/zapi_ro_user
```

### ⚠️ Security Considerations

- **SSL Verification**: Currently disabled (`verify=False`). For production, use valid SSL certificates and enable verification.
- **Network Security**: Ensure port 215 is only accessible from authorized networks.
- **Credential Rotation**: Regularly rotate API credentials in Vault.

---



## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Damini Marvin Mark

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

**[View Full License](LICENSE)**

---

## 🙏 Acknowledgements

This project wouldn't be possible without:

- **[Oracle ZFS Storage Appliance](https://www.oracle.com/storage/zfs-storage-appliances/)** - For their comprehensive REST API
- **[HashiCorp Vault](https://www.vaultproject.io/)** - Enterprise secrets management
- **[pandas](https://pandas.pydata.org/)** - Powerful data manipulation library
- **[requests](https://requests.readthedocs.io/)** - Elegant HTTP library for Python
- **[docopt](http://docopt.org/)** - Command-line interface magic
- **[tabulate](https://github.com/astanin/python-tabulate)** - Pretty-print tabular data

---

## 📬 Contact & Support


### Connect with the Maintainer

**Damini Marvin Mark**  
🌐 Website: [dmarkstorage.io](https://dmarkstorage.io)  
🐙 GitHub: [@daminimark](https://github.com/DMarkStorage)

---

