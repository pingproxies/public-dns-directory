# Public DNS Servers

[![Last Updated](https://img.shields.io/github/last-commit/pingproxies/public-dns-servers?label=updated)](https://github.com/pingproxies/public-dns-servers/commits/main)
[![License](https://img.shields.io/github/license/pingproxies/public-dns-servers)](LICENSE)
[![Stars](https://img.shields.io/github/stars/pingproxies/public-dns-servers?style=social)](https://github.com/pingproxies/public-dns-servers)

The most comprehensive and data-rich public DNS server list on GitHub. Daily-updated, organized by 160+ countries, with uptime metrics, DNSSEC status, and filtering capabilities that no other repository provides.

**Data Source:** [dnsdirectory.com](https://dnsdirectory.com)

---

## Quick Start

### Download All Servers (IPv4)

```bash
# Using wget
wget https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/resolvers/global/all.txt

# Using curl
curl -O https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/resolvers/global/all.txt
```

### Download Trusted Servers Only

```bash
wget https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/resolvers/global/trusted.txt
```

### Download by Country

```bash
# United States
wget https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/resolvers/by-country/US.txt

# Germany
wget https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/resolvers/by-country/DE.txt
```

---

## File Organization

| Directory | Format | Description |
|-----------|--------|-------------|
| `resolvers/global/` | TXT | Aggregated lists (all, trusted, dnssec, ad-blocking, etc.) |
| `resolvers/by-country/` | TXT | IPv4 servers by ISO 3166-1 alpha-2 country code |
| `resolvers/by-country-ipv6/` | TXT | IPv6 servers by country |
| `resolvers/by-continent/` | TXT | Servers by continent code (NA, EU, AS, etc.) |
| `data/` | JSON/CSV | Full metadata for programmatic access |
| `data/by-country/` | JSON | Full metadata per country |
| `data/by-continent/` | JSON | Full metadata per continent |

---

## Usage Examples

### With massdns

```bash
massdns -r resolvers/global/all.txt -t A domains.txt -o S
```

### With shuffledns

```bash
shuffledns -d example.com -r resolvers/global/trusted.txt -w wordlist.txt
```

### With dnsx

```bash
echo example.com | dnsx -r resolvers/by-country/US.txt -a -resp
```

### With dig (manual testing)

```bash
# Test a specific resolver
dig @8.8.8.8 example.com A
```

### With Python

```python
import requests

url = "https://raw.githubusercontent.com/pingproxies/public-dns-servers/main/data/resolvers.json"
data = requests.get(url).json()

for resolver in data["resolvers"][:10]:
    print(f"{resolver['ip']} - {resolver['country']} - Trusted: {resolver['trusted']}")
```

---

## Available Lists

### Global Lists

| File | Description |
|------|-------------|
| [`all.txt`](resolvers/global/all.txt) | All online IPv4 DNS servers |
| [`all-ipv6.txt`](resolvers/global/all-ipv6.txt) | All online IPv6 DNS servers |
| [`trusted.txt`](resolvers/global/trusted.txt) | Verified trusted providers (Google, Cloudflare, Quad9, etc.) |
| [`trusted-ipv6.txt`](resolvers/global/trusted-ipv6.txt) | Trusted providers - IPv6 |
| [`dnssec.txt`](resolvers/global/dnssec.txt) | DNSSEC-validating servers |
| [`dnssec-ipv6.txt`](resolvers/global/dnssec-ipv6.txt) | DNSSEC-validating - IPv6 |
| [`ad-blocking.txt`](resolvers/global/ad-blocking.txt) | Ad-blocking DNS servers |
| [`malware-blocking.txt`](resolvers/global/malware-blocking.txt) | Malware-blocking DNS servers |
| [`family-safe.txt`](resolvers/global/family-safe.txt) | Adult content filtering |
| [`high-uptime.txt`](resolvers/global/high-uptime.txt) | Servers with 99%+ uptime (30 days) |

### By Country

DNS servers organized by [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country codes.

| Country | Code | IPv4 | IPv6 |
|---------|------|------|------|
| United States | [US](resolvers/by-country/US.txt) | [US.txt](resolvers/by-country/US.txt) | [US.txt](resolvers/by-country-ipv6/US.txt) |
| Germany | [DE](resolvers/by-country/DE.txt) | [DE.txt](resolvers/by-country/DE.txt) | [DE.txt](resolvers/by-country-ipv6/DE.txt) |
| United Kingdom | [GB](resolvers/by-country/GB.txt) | [GB.txt](resolvers/by-country/GB.txt) | [GB.txt](resolvers/by-country-ipv6/GB.txt) |
| France | [FR](resolvers/by-country/FR.txt) | [FR.txt](resolvers/by-country/FR.txt) | [FR.txt](resolvers/by-country-ipv6/FR.txt) |
| Netherlands | [NL](resolvers/by-country/NL.txt) | [NL.txt](resolvers/by-country/NL.txt) | [NL.txt](resolvers/by-country-ipv6/NL.txt) |
| Japan | [JP](resolvers/by-country/JP.txt) | [JP.txt](resolvers/by-country/JP.txt) | [JP.txt](resolvers/by-country-ipv6/JP.txt) |
| Canada | [CA](resolvers/by-country/CA.txt) | [CA.txt](resolvers/by-country/CA.txt) | [CA.txt](resolvers/by-country-ipv6/CA.txt) |
| Australia | [AU](resolvers/by-country/AU.txt) | [AU.txt](resolvers/by-country/AU.txt) | [AU.txt](resolvers/by-country-ipv6/AU.txt) |

Browse [`resolvers/by-country/`](resolvers/by-country/) for the complete list (160+ countries).

### By Continent

| Continent | Code | File |
|-----------|------|------|
| Africa | AF | [`AF.txt`](resolvers/by-continent/AF.txt) |
| Asia | AS | [`AS.txt`](resolvers/by-continent/AS.txt) |
| Europe | EU | [`EU.txt`](resolvers/by-continent/EU.txt) |
| North America | NA | [`NA.txt`](resolvers/by-continent/NA.txt) |
| Oceania | OC | [`OC.txt`](resolvers/by-continent/OC.txt) |
| South America | SA | [`SA.txt`](resolvers/by-continent/SA.txt) |

---

## Data Formats

### TXT (for security tools)

Plain text files with one IP address per line. Includes a comment header with metadata.

```
# Public DNS Servers - United States (US)
# Source: https://dnsdirectory.com
# Updated: 2024-02-04T06:00:00Z
# Total: 523 servers
#
8.8.8.8
8.8.4.4
1.1.1.1
...
```

**Best for:** massdns, shuffledns, dnsx, and other DNS reconnaissance tools.

### JSON (for developers)

Full metadata including uptime statistics, DNSSEC status, and blocking capabilities.

```json
{
  "ip": "8.8.8.8",
  "version": 4,
  "country_code": "US",
  "country": "United States",
  "organization": "Google LLC",
  "trusted": true,
  "dnssec": {
    "aware": true,
    "validating": true
  },
  "blocking": {
    "ads": false,
    "malware": false,
    "adult": false
  },
  "uptime": {
    "24h": 100.0,
    "30d": 99.98,
    "90d": 99.97,
    "1y": 99.95
  }
}
```

**Files:**
- [`data/resolvers.json`](data/resolvers.json) - Complete dataset with all metadata
- [`data/resolvers-minimal.json`](data/resolvers-minimal.json) - IP + country + trusted only
- [`data/stats.json`](data/stats.json) - Repository statistics

### CSV (for analysis)

Flat format suitable for spreadsheets and database imports.

**File:** [`data/resolvers.csv`](data/resolvers.csv)

---

## Metadata Fields

| Field | Description |
|-------|-------------|
| `ip` | DNS server IP address |
| `version` | IP version (4 or 6) |
| `country_code` | ISO 3166-1 alpha-2 country code |
| `country` | Country name |
| `continent_code` | Continent code (NA, EU, AS, etc.) |
| `organization` | Operating organization/ISP |
| `domain` | Associated domain (if any) |
| `trusted` | Verified trusted provider |
| `anycast` | Uses anycast routing |
| `dnssec.aware` | DNSSEC-aware |
| `dnssec.validating` | Performs DNSSEC validation |
| `blocking.ads` | Blocks advertisements |
| `blocking.malware` | Blocks malware domains |
| `blocking.adult` | Blocks adult content |
| `uptime.24h` | Uptime percentage (last 24 hours) |
| `uptime.30d` | Uptime percentage (last 30 days) |
| `uptime.90d` | Uptime percentage (last 90 days) |
| `uptime.1y` | Uptime percentage (last year) |

---

## Update Schedule

This repository is automatically updated **twice daily** via GitHub Actions:

- **06:00 UTC**
- **18:00 UTC**

All data is sourced from [dnsdirectory.com](https://dnsdirectory.com)'s continuous testing infrastructure.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Note:** The files in `resolvers/` and `data/` directories are auto-generated. Please do not submit pull requests modifying these files directly.

---

## Related Projects

- [dnsdirectory.com](https://dnsdirectory.com) - Full DNS directory with interactive search
- [massdns](https://github.com/blechschmidt/massdns) - High-performance DNS stub resolver
- [shuffledns](https://github.com/projectdiscovery/shuffledns) - Subdomain enumeration using massdns
- [dnsx](https://github.com/projectdiscovery/dnsx) - Fast and multi-purpose DNS toolkit

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Data provided by [dnsdirectory.com](https://dnsdirectory.com) and the [Ping Proxies](https://pingproxies.com) team.
