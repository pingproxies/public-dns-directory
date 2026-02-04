# Contributing to Public DNS Servers

Thank you for your interest in contributing to the Public DNS Servers repository!

## Important Note

The files in `resolvers/` and `data/` directories are **automatically generated** from the [dnsdirectory.com](https://dnsdirectory.com) API. Please do not submit pull requests that directly modify these files, as they will be overwritten by the next automated update.

## How to Contribute

### Reporting Issues

If you find incorrect data or issues with the repository:

1. Check if an issue already exists for your problem
2. Use the appropriate issue template:
   - **Bug Report**: For data issues, broken files, or repository problems
   - **Server Submission**: To suggest adding a new DNS server

### Suggesting Improvements

We welcome suggestions for:

- Documentation improvements
- New categories or filtering options
- Script enhancements
- Additional file formats

Please open an issue to discuss your idea before submitting a pull request.

### Pull Requests

Pull requests are welcome for:

- Documentation updates (README, CONTRIBUTING, etc.)
- Script improvements (`scripts/` directory)
- GitHub Actions workflow enhancements
- New issue/PR templates

**Not accepted:**
- Direct modifications to `resolvers/` or `data/` files
- Changes that would break the automated update process

### Code Style

For Python code in the `scripts/` directory:

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for functions and classes
- Keep code simple and readable

## Submitting a New DNS Server

If you know of a public DNS server that should be included:

1. Use the "Server Submission" issue template
2. Provide:
   - DNS server IP address
   - Provider/organization name
   - Features (DNSSEC, ad-blocking, etc.)
   - Link to official documentation (if available)

Submitted servers will be reviewed and added to [dnsdirectory.com](https://dnsdirectory.com), which will then propagate to this repository.

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to make this resource better for everyone.
