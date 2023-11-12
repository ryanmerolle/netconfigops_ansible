# Ansible Collection - ryanmerolle.netconfigops

Network Configuration Ops Ansible Collection

## Upcoming Features

- **Platforms:**:
  - Arista EOS
  - Cisco IOS variants
  - Cisco NXOS
  - TBD
- **Configuration Remediation Building:** Build path from intended to running configuration (Does not apply configuration)
- **Configuration Drift Audit:** Build diff view of intended vs running configuration (Does not apply configuration)
- **Configuration Backout Building:** Build path to backout configuration given intended and running configurations
- **Leverage Off Box Backup:** Build all of the above using existing running configuration backups
- **Backup Device:** Backup the device no matter the platform
- **Validate Intended Configuration:** Validate that the configuration order, spacing, and syntax is valid for the platform
- **Apply Configuration:**
  - Full configuration replace
  - Only configuration remediation
- **Apply Configuration Backout:**
  - Full configuration replace
  - Only configuration remediation

## Dependencies

### Python

- ansible / ansible-core
- hier_config

### Ansible

- ansible.netcommon
- arista.eos
- cisco.ios
- cisco.nxos

## Dev Dependencies

- mkdocs
