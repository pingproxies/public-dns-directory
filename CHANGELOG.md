# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.0] - 2024-02-04

### Added

- Initial repository setup
- Automated twice-daily updates via GitHub Actions
- Multiple output formats:
  - TXT files for DNS tools (massdns, shuffledns, dnsx)
  - JSON files with full metadata
  - CSV file for data analysis
- Organization by geography:
  - Global aggregated lists
  - Per-country files (160+ countries)
  - Per-continent files (6 continents)
  - IPv6 variants
- Curated feature lists:
  - `trusted.txt` - Verified trusted providers
  - `dnssec.txt` - DNSSEC-validating servers
  - `ad-blocking.txt` - Ad-blocking DNS
  - `malware-blocking.txt` - Malware protection
  - `family-safe.txt` - Adult content filtering
  - `high-uptime.txt` - High reliability servers
- Rich metadata including:
  - Uptime statistics (24h, 30d, 90d, 1y)
  - DNSSEC awareness and validation status
  - Blocking capabilities
  - Organization/ISP information
  - Anycast detection
- Documentation:
  - Comprehensive README with usage examples
  - Contributing guidelines
  - Security policy
- GitHub issue templates for bug reports and server submissions
