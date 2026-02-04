<div align="center">

# Public DNS Servers List by Ping Proxies

### The most comprehensive public DNS server list on GitHub

[![Servers](https://img.shields.io/badge/servers-9,879-blue?style=for-the-badge)](data/stats.json)
[![Countries](https://img.shields.io/badge/countries-153-green?style=for-the-badge)](resolvers/by-country/)
[![Updated](https://img.shields.io/github/last-commit/pingproxies/public-dns-directory?style=for-the-badge&label=updated)](https://github.com/pingproxies/public-dns-directory/commits/main)

[![License](https://img.shields.io/github/license/pingproxies/public-dns-directory?style=flat-square)](LICENSE)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/pingproxies/public-dns-directory/update-resolvers.yml?style=flat-square&label=auto-update)](https://github.com/pingproxies/public-dns-directory/actions)
[![Stars](https://img.shields.io/github/stars/pingproxies/public-dns-directory?style=flat-square)](https://github.com/pingproxies/public-dns-directory/stargazers)

<br/>

![About Ping Illustration](images/About%20Ping%20Illustration.svg)

<br/>

**Daily-updated DNS resolvers organized by 153 countries with uptime metrics, DNSSEC status, and content filtering capabilities.**

[Quick Start](#quick-start) · [Available Lists](#available-lists) · [Usage Examples](#usage-examples) · [Data Formats](#data-formats)

---

**Data Source:** [dnsdirectory.com](https://dnsdirectory.com)

</div>

## Quick Start

Download resolver lists instantly:

```bash
# All servers (IPv4)
curl -O https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/resolvers/global/all.txt

# Trusted providers only (Google, Cloudflare, Quad9, etc.)
curl -O https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/resolvers/global/trusted.txt

# By country (e.g., United States)
curl -O https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/resolvers/by-country/US.txt
```

## Features

| Feature | Description |
|---------|-------------|
| **9,800+ Servers** | Comprehensive coverage of public DNS resolvers worldwide |
| **153 Countries** | Organized by ISO 3166-1 alpha-2 country codes |
| **Rich Metadata** | Uptime (24h/30d/90d/1y), DNSSEC, blocking capabilities |
| **Multiple Formats** | TXT for tools, JSON for developers, CSV for analysis |
| **Auto-Updated** | Refreshed twice daily via GitHub Actions |
| **Curated Lists** | Trusted, DNSSEC, ad-blocking, malware-blocking, family-safe |

## Available Lists

### Global Lists

| List | Description | Download |
|------|-------------|----------|
| **All Servers** | Complete IPv4 resolver list | [`all.txt`](resolvers/global/all.txt) |
| **Trusted** | Verified providers (Google, Cloudflare, Quad9) | [`trusted.txt`](resolvers/global/trusted.txt) |
| **DNSSEC** | DNSSEC-validating servers | [`dnssec.txt`](resolvers/global/dnssec.txt) |
| **Ad-Blocking** | Blocks advertisements | [`ad-blocking.txt`](resolvers/global/ad-blocking.txt) |
| **Malware-Blocking** | Blocks malicious domains | [`malware-blocking.txt`](resolvers/global/malware-blocking.txt) |
| **Family-Safe** | Adult content filtering | [`family-safe.txt`](resolvers/global/family-safe.txt) |
| **High Uptime** | 99%+ uptime (30 days) | [`high-uptime.txt`](resolvers/global/high-uptime.txt) |

### By Country

Servers organized by [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country codes.

| Country | IPv4 | JSON |
|---------|------|------|
| United States | [`US.txt`](resolvers/by-country/US.txt) | [`US.json`](data/by-country/US.json) |
| Germany | [`DE.txt`](resolvers/by-country/DE.txt) | [`DE.json`](data/by-country/DE.json) |
| United Kingdom | [`GB.txt`](resolvers/by-country/GB.txt) | [`GB.json`](data/by-country/GB.json) |
| France | [`FR.txt`](resolvers/by-country/FR.txt) | [`FR.json`](data/by-country/FR.json) |
| Netherlands | [`NL.txt`](resolvers/by-country/NL.txt) | [`NL.json`](data/by-country/NL.json) |
| Japan | [`JP.txt`](resolvers/by-country/JP.txt) | [`JP.json`](data/by-country/JP.json) |
| Canada | [`CA.txt`](resolvers/by-country/CA.txt) | [`CA.json`](data/by-country/CA.json) |
| Australia | [`AU.txt`](resolvers/by-country/AU.txt) | [`AU.json`](data/by-country/AU.json) |

**[Browse all 153 countries →](resolvers/by-country/)**

### By Continent

| Continent | File |
|-----------|------|
| Africa | [`AF.txt`](resolvers/by-continent/AF.txt) |
| Asia | [`AS.txt`](resolvers/by-continent/AS.txt) |
| Europe | [`EU.txt`](resolvers/by-continent/EU.txt) |
| North America | [`NA.txt`](resolvers/by-continent/NA.txt) |
| Oceania | [`OC.txt`](resolvers/by-continent/OC.txt) |
| South America | [`SA.txt`](resolvers/by-continent/SA.txt) |

## Usage Examples

### Security Tools

```bash
# massdns - High-performance DNS resolution
massdns -r resolvers/global/all.txt -t A domains.txt -o S

# shuffledns - Subdomain enumeration
shuffledns -d example.com -r resolvers/global/trusted.txt -w wordlist.txt

# dnsx - DNS toolkit
cat subdomains.txt | dnsx -r resolvers/by-country/US.txt -a -resp
```

### Python

```python
import requests

url = "https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/data/resolvers.json"
data = requests.get(url).json()

# Get all trusted DNSSEC servers
trusted_dnssec = [
    r for r in data["resolvers"]
    if r["trusted"] and r["dnssec"]["validating"]
]

for server in trusted_dnssec[:5]:
    print(f"{server['ip']} - {server['organization']}")
```

### cURL / Shell

```bash
# Get server count
curl -s https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/data/stats.json | jq '.totals.servers'

# List all US servers
curl -s https://raw.githubusercontent.com/pingproxies/public-dns-directory/main/resolvers/by-country/US.txt | grep -v "^#"
```

## Data Formats

### TXT — For Security Tools

One IP per line, compatible with massdns, shuffledns, dnsx.

```
# Public DNS Servers - United States (US)
# Source: https://dnsdirectory.com
# Updated: 2024-02-04T06:00:00Z
# Total: 1,234 servers
#
8.8.8.8
8.8.4.4
1.1.1.1
```

### JSON — For Developers

Full metadata with nested structure.

```json
{
  "ip": "8.8.8.8",
  "version": 4,
  "country_code": "US",
  "country": "United States",
  "organization": "Google LLC",
  "trusted": true,
  "dnssec": { "aware": true, "validating": true },
  "blocking": { "ads": false, "malware": false, "adult": false },
  "uptime": { "24h": 100.0, "30d": 99.98, "90d": 99.97, "1y": 99.95 }
}
```

**Files:**
- [`resolvers.json`](data/resolvers.json) — Complete dataset
- [`resolvers-minimal.json`](data/resolvers-minimal.json) — IP + country + trusted
- [`stats.json`](data/stats.json) — Repository statistics

### CSV — For Analysis

Flat format for spreadsheets and databases: [`resolvers.csv`](data/resolvers.csv)

## File Structure

```
├── resolvers/
│   ├── global/           # Aggregated lists (all, trusted, dnssec, etc.)
│   ├── by-country/       # IPv4 by country code (US.txt, DE.txt, ...)
│   ├── by-country-ipv6/  # IPv6 by country code
│   └── by-continent/     # By continent (NA.txt, EU.txt, ...)
└── data/
    ├── resolvers.json    # Complete dataset with metadata
    ├── resolvers.csv     # Flat CSV export
    ├── stats.json        # Statistics
    ├── by-country/       # JSON per country
    └── by-continent/     # JSON per continent
```

## Update Schedule

This repository is automatically updated **twice daily** via GitHub Actions:

| Schedule | Time |
|----------|------|
| Morning | 06:00 UTC |
| Evening | 18:00 UTC |

## Related Projects

- [dnsdirectory.com](https://dnsdirectory.com) — Full DNS directory with interactive search
- [massdns](https://github.com/blechschmidt/massdns) — High-performance DNS stub resolver
- [shuffledns](https://github.com/projectdiscovery/shuffledns) — Subdomain enumeration
- [dnsx](https://github.com/projectdiscovery/dnsx) — Fast DNS toolkit

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

> **Note:** Files in `resolvers/` and `data/` are auto-generated. Do not edit directly.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Data provided by [dnsdirectory.com](https://dnsdirectory.com) and [Ping Proxies](https://pingproxies.com)**

</div>
