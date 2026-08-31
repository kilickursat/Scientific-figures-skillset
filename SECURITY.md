# Security and Privacy Policy

## Supported versions

Security fixes are applied to the latest released version and the default branch.

## Reporting a vulnerability

Report suspected vulnerabilities privately to the repository maintainer rather than opening a public issue. Include the affected file, reproduction steps, impact, and a minimal proof of concept that does not expose confidential data.

## Threat model

The canonical skill and bundled Python utilities operate on local files and do not require network access. Primary risks include:

- executing unreviewed plotting code supplied by a third party;
- path traversal or unintended overwrite during installation or scaffolding;
- disclosure of confidential manuscripts, participant data, proprietary figures, credentials, or unpublished site information;
- malicious SVG external references or active content;
- oversized or malformed image/PDF inputs that consume excessive resources;
- fabricated provenance or misleading metadata supplied by an operator.

## Safe use

- Review skill files and scripts before installation.
- Run unknown code in a sandbox with restricted network and filesystem access.
- Keep raw confidential data outside public repositories.
- Strip credentials and identifying metadata before sharing artifacts.
- Treat manifests as signed declarations, not proof of honesty.
- Use virus and file-format scanning appropriate to your institution.
- Do not enable automatic overwrites unless the destination has been reviewed.

The QC tool reports external SVG references and malformed files but is not a malware scanner or research-integrity oracle.
