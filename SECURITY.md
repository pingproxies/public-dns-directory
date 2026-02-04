# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in this repository or its automation, please report it responsibly:

**Email:** security@dnsdirectory.com

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and work to address the issue promptly.

## Data Integrity

All DNS server data in this repository is sourced from [dnsdirectory.com](https://dnsdirectory.com)'s validated testing infrastructure. The data goes through the following validation:

1. **Online Status**: Only servers that respond to DNS queries are included
2. **Response Validation**: Servers must return valid DNS responses
3. **Continuous Monitoring**: Uptime is tracked over 24h, 30d, 90d, and 1y periods

## Trusted Providers

Servers marked as "trusted" have been manually verified to belong to known, reputable DNS providers such as:

- Google Public DNS
- Cloudflare DNS
- Quad9
- OpenDNS
- AdGuard DNS

## Using This Data

When using DNS servers from this repository:

- **For security research**: Use the `trusted.txt` list for more reliable results
- **For production**: Verify servers independently before deployment
- **For testing**: Any server list is suitable for development/testing purposes

## Disclaimer

While we strive to maintain accurate data, we cannot guarantee the security or reliability of any individual DNS server. Use this data at your own risk and always verify servers for your specific use case.
