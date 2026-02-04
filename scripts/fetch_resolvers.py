#!/usr/bin/env python3
"""
DNS Resolver Fetcher

Fetches DNS server data from dnsdirectory.com API and generates
organized output files in multiple formats (TXT, JSON, CSV).

Usage:
    DNS_API_ENDPOINT=https://... python fetch_resolvers.py
"""

import csv
import json
import logging
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """Configuration settings loaded from environment variables."""
    api_endpoint: str
    max_retries: int = 3
    retry_delay: int = 30
    request_timeout: int = 60
    per_page: int = 1000
    rate_limit_delay: float = 1.0
    high_uptime_threshold: float = 99.0

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        endpoint = os.environ.get("DNS_API_ENDPOINT")
        if not endpoint:
            raise ValueError("DNS_API_ENDPOINT environment variable is required")
        return cls(api_endpoint=endpoint)


# ============================================================================
# DATA MODELS
# ============================================================================

def _to_float(value, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass
class Resolver:
    """Transformed resolver data model."""
    ip: str
    version: int
    country_code: str
    country: str
    continent_code: str
    continent: str
    organization: str
    domain: str
    trusted: bool
    anycast: bool
    dnssec_aware: bool
    dnssec_validating: bool
    ad_blocking: bool
    malware_blocking: bool
    adult_blocking: bool
    uptime_24h: float
    uptime_30d: float
    uptime_90d: float
    uptime_1y: float

    @classmethod
    def from_api_response(cls, data: dict) -> "Resolver":
        """Transform API response to our data model."""
        return cls(
            ip=data.get("dns_server_ip_address", ""),
            version=data.get("dns_server_ip_address_version", 4),
            country_code=data.get("country_id", ""),
            country=data.get("country_name", ""),
            continent_code=data.get("continent_id", ""),
            continent=data.get("continent_name", ""),
            organization=data.get("dns_server_organization", ""),
            domain=data.get("dns_server_domain", ""),
            trusted=data.get("dns_server_is_trusted", False),
            anycast=data.get("dns_server_is_anycast", False),
            dnssec_aware=data.get("dns_server_dnssec_aware", False),
            dnssec_validating=data.get("dns_server_dnssec_validating", False),
            ad_blocking=data.get("dns_server_is_ad_blocking", False),
            malware_blocking=data.get("dns_server_is_malware_blocking", False),
            adult_blocking=data.get("dns_server_is_porn_blocking", False),
            uptime_24h=_to_float(data.get("dns_server_uptime_24h")),
            uptime_30d=_to_float(data.get("dns_server_uptime_30d")),
            uptime_90d=_to_float(data.get("dns_server_uptime_90d")),
            uptime_1y=_to_float(data.get("dns_server_uptime_1y")),
        )

    def to_json_dict(self) -> dict:
        """Convert to JSON-friendly dictionary with nested structure."""
        return {
            "ip": self.ip,
            "version": self.version,
            "country_code": self.country_code,
            "country": self.country,
            "continent_code": self.continent_code,
            "continent": self.continent,
            "organization": self.organization,
            "domain": self.domain,
            "trusted": self.trusted,
            "anycast": self.anycast,
            "dnssec": {
                "aware": self.dnssec_aware,
                "validating": self.dnssec_validating,
            },
            "blocking": {
                "ads": self.ad_blocking,
                "malware": self.malware_blocking,
                "adult": self.adult_blocking,
            },
            "uptime": {
                "24h": self.uptime_24h,
                "30d": self.uptime_30d,
                "90d": self.uptime_90d,
                "1y": self.uptime_1y,
            },
        }

    def to_csv_row(self) -> dict:
        """Convert to flat dictionary for CSV export."""
        return {
            "ip": self.ip,
            "version": self.version,
            "country_code": self.country_code,
            "country": self.country,
            "continent_code": self.continent_code,
            "continent": self.continent,
            "organization": self.organization,
            "domain": self.domain,
            "trusted": self.trusted,
            "anycast": self.anycast,
            "dnssec_aware": self.dnssec_aware,
            "dnssec_validating": self.dnssec_validating,
            "ad_blocking": self.ad_blocking,
            "malware_blocking": self.malware_blocking,
            "adult_blocking": self.adult_blocking,
            "uptime_24h": self.uptime_24h,
            "uptime_30d": self.uptime_30d,
            "uptime_90d": self.uptime_90d,
            "uptime_1y": self.uptime_1y,
        }


# ============================================================================
# API CLIENT
# ============================================================================

class DNSApiClient:
    """Client for fetching data from DNS Directory API."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def fetch_all_servers(self) -> list[Resolver]:
        """Fetch all online DNS servers with pagination."""
        all_servers = []
        page = 1

        while True:
            self.logger.info(f"Fetching page {page}...")
            data = self._fetch_page(page)
            servers = data.get("data", [])

            for server in servers:
                if server.get("dns_server_is_online"):
                    all_servers.append(Resolver.from_api_response(server))

            self.logger.info(f"Page {page}: {len(servers)} servers fetched")

            if len(servers) < self.config.per_page:
                break

            page += 1
            time.sleep(self.config.rate_limit_delay)

        self.logger.info(f"Total: {len(all_servers)} online servers fetched")
        return all_servers

    def _fetch_page(self, page: int) -> dict:
        """Fetch a single page with retry logic."""
        params = {
            "dns_server_is_online": "true",
            "per_page": self.config.per_page,
            "page": page,
            "sort_by": "country_id",
        }

        for attempt in range(self.config.max_retries):
            try:
                response = self.session.get(
                    self.config.api_endpoint,
                    params=params,
                    timeout=self.config.request_timeout,
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    raise


# ============================================================================
# FILE GENERATOR
# ============================================================================

class FileGenerator:
    """Generates output files in various formats."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.logger = logging.getLogger(__name__)

    def generate_all(self, resolvers: list[Resolver], config: Config) -> dict:
        """Generate all output files and return statistics."""
        stats = self._calculate_stats(resolvers, config)

        # Generate TXT files
        self._generate_global_txt_files(resolvers, config)
        self._generate_country_txt_files(resolvers)
        self._generate_country_ipv6_txt_files(resolvers)
        self._generate_continent_txt_files(resolvers)

        # Generate JSON files
        self._generate_main_json(resolvers, stats)
        self._generate_minimal_json(resolvers)
        self._generate_country_json_files(resolvers)
        self._generate_continent_json_files(resolvers)
        self._generate_stats_json(stats)

        # Generate CSV file
        self._generate_csv(resolvers)

        return stats

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def _calculate_stats(self, resolvers: list[Resolver], config: Config) -> dict:
        """Calculate repository statistics."""
        ipv4 = [r for r in resolvers if r.version == 4]
        ipv6 = [r for r in resolvers if r.version == 6]

        countries = defaultdict(int)
        continents = defaultdict(lambda: {"name": "", "count": 0})
        organizations = defaultdict(int)

        for r in resolvers:
            if r.country_code:
                countries[r.country_code] += 1
            if r.continent_code:
                continents[r.continent_code]["name"] = r.continent
                continents[r.continent_code]["count"] += 1
            if r.organization:
                organizations[r.organization] += 1

        # Sort countries by count
        sorted_countries = sorted(countries.items(), key=lambda x: -x[1])
        top_countries = {}
        for code, count in sorted_countries:
            resolver = next((r for r in resolvers if r.country_code == code), None)
            if resolver:
                top_countries[code] = {"name": resolver.country, "count": count}

        # Sort organizations by count
        sorted_orgs = sorted(organizations.items(), key=lambda x: -x[1])[:20]
        top_orgs = [{"name": name, "count": count} for name, count in sorted_orgs]

        return {
            "last_updated": self.timestamp,
            "update_frequency": "twice daily",
            "data_source": "https://dnsdirectory.com",
            "totals": {
                "servers": len(resolvers),
                "servers_ipv4": len(ipv4),
                "servers_ipv6": len(ipv6),
                "countries": len(countries),
                "continents": len(continents),
                "organizations": len(organizations),
            },
            "by_feature": {
                "online": len(resolvers),
                "trusted": len([r for r in resolvers if r.trusted]),
                "dnssec_aware": len([r for r in resolvers if r.dnssec_aware]),
                "dnssec_validating": len([r for r in resolvers if r.dnssec_validating]),
                "ad_blocking": len([r for r in resolvers if r.ad_blocking]),
                "malware_blocking": len([r for r in resolvers if r.malware_blocking]),
                "adult_blocking": len([r for r in resolvers if r.adult_blocking]),
                "anycast": len([r for r in resolvers if r.anycast]),
                "high_uptime_30d": len([r for r in resolvers if r.uptime_30d >= config.high_uptime_threshold]),
            },
            "by_continent": {
                code: data for code, data in sorted(continents.items())
            },
            "by_country": top_countries,
            "top_organizations": top_orgs,
        }

    # -------------------------------------------------------------------------
    # TXT File Generators
    # -------------------------------------------------------------------------

    def _generate_txt_header(self, title: str, count: int, usage_example: Optional[str] = None) -> str:
        """Generate standard header for TXT files."""
        lines = [
            f"# {title}",
            "# Source: https://dnsdirectory.com",
            f"# Updated: {self.timestamp}",
            f"# Total: {count} servers",
            "#",
        ]
        if usage_example:
            lines.append(f"# Usage: {usage_example}")
            lines.append("#")
        return "\n".join(lines)

    def _write_txt_file(self, relative_path: str, title: str, resolvers: list[Resolver], usage_example: Optional[str] = None) -> None:
        """Write a TXT file with header and IP addresses."""
        ips = sorted(set(r.ip for r in resolvers))
        header = self._generate_txt_header(title, len(ips), usage_example)
        content = header + "\n" + "\n".join(ips) + "\n"
        self._write_file(relative_path, content)

    def _generate_global_txt_files(self, resolvers: list[Resolver], config: Config) -> None:
        """Generate global TXT files."""
        self.logger.info("Generating global TXT files...")

        ipv4 = [r for r in resolvers if r.version == 4]
        ipv6 = [r for r in resolvers if r.version == 6]

        # All servers
        self._write_txt_file(
            "resolvers/global/all.txt",
            "Public DNS Servers - All IPv4",
            ipv4,
            "massdns -r all.txt -t A domains.txt",
        )
        self._write_txt_file(
            "resolvers/global/all-ipv6.txt",
            "Public DNS Servers - All IPv6",
            ipv6,
        )

        # Trusted servers
        self._write_txt_file(
            "resolvers/global/trusted.txt",
            "Public DNS Servers - Trusted Providers (IPv4)",
            [r for r in ipv4 if r.trusted],
            "massdns -r trusted.txt -t A domains.txt",
        )
        self._write_txt_file(
            "resolvers/global/trusted-ipv6.txt",
            "Public DNS Servers - Trusted Providers (IPv6)",
            [r for r in ipv6 if r.trusted],
        )

        # DNSSEC validating
        self._write_txt_file(
            "resolvers/global/dnssec.txt",
            "Public DNS Servers - DNSSEC Validating (IPv4)",
            [r for r in ipv4 if r.dnssec_validating],
        )
        self._write_txt_file(
            "resolvers/global/dnssec-ipv6.txt",
            "Public DNS Servers - DNSSEC Validating (IPv6)",
            [r for r in ipv6 if r.dnssec_validating],
        )

        # Ad-blocking
        self._write_txt_file(
            "resolvers/global/ad-blocking.txt",
            "Public DNS Servers - Ad Blocking (IPv4)",
            [r for r in ipv4 if r.ad_blocking],
        )

        # Malware-blocking
        self._write_txt_file(
            "resolvers/global/malware-blocking.txt",
            "Public DNS Servers - Malware Blocking (IPv4)",
            [r for r in ipv4 if r.malware_blocking],
        )

        # Family-safe (adult content blocking)
        self._write_txt_file(
            "resolvers/global/family-safe.txt",
            "Public DNS Servers - Family Safe / Adult Blocking (IPv4)",
            [r for r in ipv4 if r.adult_blocking],
        )

        # High uptime
        self._write_txt_file(
            "resolvers/global/high-uptime.txt",
            f"Public DNS Servers - High Uptime >={config.high_uptime_threshold}% (IPv4)",
            [r for r in ipv4 if r.uptime_30d >= config.high_uptime_threshold],
        )

    def _generate_country_txt_files(self, resolvers: list[Resolver]) -> None:
        """Generate per-country TXT files for IPv4."""
        self.logger.info("Generating country TXT files (IPv4)...")

        by_country = defaultdict(list)
        for r in resolvers:
            if r.version == 4 and r.country_code:
                by_country[r.country_code].append(r)

        for code, country_resolvers in sorted(by_country.items()):
            country_name = country_resolvers[0].country if country_resolvers else code
            self._write_txt_file(
                f"resolvers/by-country/{code}.txt",
                f"Public DNS Servers - {country_name} ({code})",
                country_resolvers,
                f"massdns -r {code}.txt -t A domains.txt",
            )

    def _generate_country_ipv6_txt_files(self, resolvers: list[Resolver]) -> None:
        """Generate per-country TXT files for IPv6."""
        self.logger.info("Generating country TXT files (IPv6)...")

        by_country = defaultdict(list)
        for r in resolvers:
            if r.version == 6 and r.country_code:
                by_country[r.country_code].append(r)

        for code, country_resolvers in sorted(by_country.items()):
            country_name = country_resolvers[0].country if country_resolvers else code
            self._write_txt_file(
                f"resolvers/by-country-ipv6/{code}.txt",
                f"Public DNS Servers - {country_name} ({code}) - IPv6",
                country_resolvers,
            )

    def _generate_continent_txt_files(self, resolvers: list[Resolver]) -> None:
        """Generate per-continent TXT files."""
        self.logger.info("Generating continent TXT files...")

        by_continent = defaultdict(list)
        for r in resolvers:
            if r.continent_code:
                by_continent[r.continent_code].append(r)

        for code, continent_resolvers in sorted(by_continent.items()):
            continent_name = continent_resolvers[0].continent if continent_resolvers else code
            self._write_txt_file(
                f"resolvers/by-continent/{code}.txt",
                f"Public DNS Servers - {continent_name} ({code})",
                continent_resolvers,
                f"massdns -r {code}.txt -t A domains.txt",
            )

    # -------------------------------------------------------------------------
    # JSON File Generators
    # -------------------------------------------------------------------------

    def _generate_main_json(self, resolvers: list[Resolver], stats: dict) -> None:
        """Generate the main resolvers.json file."""
        self.logger.info("Generating resolvers.json...")

        data = {
            "metadata": {
                "source": "https://dnsdirectory.com",
                "generated_at": self.timestamp,
                "total_servers": len(resolvers),
                "total_countries": stats["totals"]["countries"],
                "total_continents": stats["totals"]["continents"],
            },
            "statistics": {
                "by_ip_version": {
                    "ipv4": stats["totals"]["servers_ipv4"],
                    "ipv6": stats["totals"]["servers_ipv6"],
                },
                "by_feature": {
                    "trusted": stats["by_feature"]["trusted"],
                    "dnssec_validating": stats["by_feature"]["dnssec_validating"],
                    "ad_blocking": stats["by_feature"]["ad_blocking"],
                    "malware_blocking": stats["by_feature"]["malware_blocking"],
                    "adult_blocking": stats["by_feature"]["adult_blocking"],
                },
                "top_countries": [
                    {"code": code, "name": info["name"], "count": info["count"]}
                    for code, info in list(stats["by_country"].items())[:10]
                ],
            },
            "resolvers": [r.to_json_dict() for r in resolvers],
        }

        self._write_json_file("data/resolvers.json", data)

    def _generate_minimal_json(self, resolvers: list[Resolver]) -> None:
        """Generate the minimal resolvers-minimal.json file."""
        self.logger.info("Generating resolvers-minimal.json...")

        data = {
            "generated_at": self.timestamp,
            "resolvers": [
                {"ip": r.ip, "country": r.country_code, "trusted": r.trusted}
                for r in resolvers
            ],
        }

        self._write_json_file("data/resolvers-minimal.json", data)

    def _generate_country_json_files(self, resolvers: list[Resolver]) -> None:
        """Generate per-country JSON files."""
        self.logger.info("Generating country JSON files...")

        by_country = defaultdict(list)
        for r in resolvers:
            if r.country_code:
                by_country[r.country_code].append(r)

        for code, country_resolvers in sorted(by_country.items()):
            first = country_resolvers[0]
            data = {
                "metadata": {
                    "country_code": code,
                    "country_name": first.country,
                    "continent_code": first.continent_code,
                    "continent_name": first.continent,
                    "generated_at": self.timestamp,
                    "total_servers": len(country_resolvers),
                },
                "resolvers": [r.to_json_dict() for r in country_resolvers],
            }
            self._write_json_file(f"data/by-country/{code}.json", data)

    def _generate_continent_json_files(self, resolvers: list[Resolver]) -> None:
        """Generate per-continent JSON files."""
        self.logger.info("Generating continent JSON files...")

        by_continent = defaultdict(list)
        for r in resolvers:
            if r.continent_code:
                by_continent[r.continent_code].append(r)

        for code, continent_resolvers in sorted(by_continent.items()):
            first = continent_resolvers[0]
            data = {
                "metadata": {
                    "continent_code": code,
                    "continent_name": first.continent,
                    "generated_at": self.timestamp,
                    "total_servers": len(continent_resolvers),
                },
                "resolvers": [r.to_json_dict() for r in continent_resolvers],
            }
            self._write_json_file(f"data/by-continent/{code}.json", data)

    def _generate_stats_json(self, stats: dict) -> None:
        """Generate the stats.json file."""
        self.logger.info("Generating stats.json...")
        self._write_json_file("data/stats.json", stats)

    # -------------------------------------------------------------------------
    # CSV File Generator
    # -------------------------------------------------------------------------

    def _generate_csv(self, resolvers: list[Resolver]) -> None:
        """Generate the resolvers.csv file."""
        self.logger.info("Generating resolvers.csv...")

        file_path = self.base_path / "data" / "resolvers.csv"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "ip", "version", "country_code", "country", "continent_code", "continent",
            "organization", "domain", "trusted", "anycast", "dnssec_aware", "dnssec_validating",
            "ad_blocking", "malware_blocking", "adult_blocking",
            "uptime_24h", "uptime_30d", "uptime_90d", "uptime_1y",
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in resolvers:
                writer.writerow(r.to_csv_row())

        self.logger.debug(f"Wrote {file_path}")

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def _write_file(self, relative_path: str, content: str) -> None:
        """Write content to file, creating directories as needed."""
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self.logger.debug(f"Wrote {file_path}")

    def _write_json_file(self, relative_path: str, data: dict) -> None:
        """Write JSON data to file."""
        content = json.dumps(data, indent=2, ensure_ascii=False)
        self._write_file(relative_path, content + "\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config = Config.from_env()
        logger.info("Configuration loaded successfully")

        # Fetch data from API
        client = DNSApiClient(config)
        resolvers = client.fetch_all_servers()

        if not resolvers:
            logger.error("No resolvers fetched from API")
            sys.exit(1)

        # Generate output files
        base_path = Path(__file__).parent.parent
        generator = FileGenerator(base_path)
        stats = generator.generate_all(resolvers, config)

        # Print summary
        logger.info("=" * 60)
        logger.info("Generation complete!")
        logger.info(f"  Total servers: {stats['totals']['servers']}")
        logger.info(f"  IPv4 servers: {stats['totals']['servers_ipv4']}")
        logger.info(f"  IPv6 servers: {stats['totals']['servers_ipv6']}")
        logger.info(f"  Countries: {stats['totals']['countries']}")
        logger.info(f"  Continents: {stats['totals']['continents']}")
        logger.info("=" * 60)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
