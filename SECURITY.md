# Security

This version is a single-owner **loopback-only** application, not an internet-ready multi-tenant SaaS.
It uses local file permissions and SQLite; data are not yet encrypted at rest.
Do not port-forward it or expose it on an untrusted network. Do not host this version publicly.
No provider keys are required. Saved personal DOB and goals remain outside Git.

Agent plans default to OBSERVE, stage only under the local profile workspace and do not install
global skills or perform changes to external systems.

Security issues: open a private GitHub vulnerability report for the repository owner;
do not disclose credentials or private user data in public issues.
