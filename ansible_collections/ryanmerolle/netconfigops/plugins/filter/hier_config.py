from ansible.errors import AnsibleFilterError
from hier_config import Host

def load_host_configs(running_config_text, generated_config_text):
    """
    Creates a Host object and loads running and generated configuration texts.

    Parameters:
    - running_config_text (str): The current running configuration of the host.
    - generated_config_text (str): The new configuration generated for the host.

    Returns:
    - Host: A hier_config Host object loaded with the running and generated configurations.

    Usage:
    host = load_host_configs(running_config, generated_config)
    """
    host = Host(hostname="test_host", os="nxos")
    host.load_running_config(config_text=running_config_text)
    host.load_generated_config(config_text=generated_config_text)
    return host


def unified_diff_filter(running_config_text, generated_config_text):
    """
    Generates a unified diff view between running and generated configurations using hier_config.

    Parameters:
    - running_config_text (str): The current running configuration of the host.
    - generated_config_text (str): The new configuration generated for the host.

    Returns:
    - str: Unified diff as a string.

    Raises:
    - AnsibleFilterError: If there is an error in generating the diff.

    Usage:
    diff = unified_diff_filter(running_config, generated_config)
    """
    try:
        host = load_host_configs(running_config_text, generated_config_text)
        diff_config = list(host.running_config.unified_diff(host.generated_config))
        return "\n".join(diff_config) + "\n"
    except Exception as e:
        raise AnsibleFilterError(f"Error generating unified diff: {e}")


def remediation_config_filter(running_config_text, generated_config_text):
    """
    Generates a remediation configuration using hier_config.

    Parameters:
    - running_config_text (str): The current running configuration of the host.
    - generated_config_text (str): The new configuration generated for the host.

    Returns:
    - str: Remediation configuration as a string.

    Raises:
    - AnsibleFilterError: If there is an error in generating the remediation config.

    Usage:
    remediation_config = remediation_config_filter(running_config, generated_config)
    """
    try:
        host = load_host_configs(running_config_text, generated_config_text)
        remediation_config = host.remediation_config_filtered_text(include_tags={}, exclude_tags={})
        return remediation_config + "\n"
    except Exception as e:
        raise AnsibleFilterError(f"Error generating remediation config: {e}")


def rollback_config_filter(running_config_text, generated_config_text):
    """
    Generates a rollback configuration using hier_config.

    Parameters:
    - running_config_text (str): The current running configuration of the host.
    - generated_config_text (str): The new configuration generated for the host.

    Returns:
    - str: Rollback configuration as a string.

    Raises:
    - AnsibleFilterError: If there is an error in generating the rollback config.

    Usage:
    rollback_config = rollback_config_filter(running_config, generated_config)
    """
    try:
        host = load_host_configs(running_config_text, generated_config_text)
        rollback_config = host.rollback_config().all_children_sorted()
        rollback_lines = [line.cisco_style_text() for line in rollback_config]
        return "\n".join(rollback_lines) + "\n"
    except Exception as e:
        raise AnsibleFilterError(f"Error generating rollback config: {e}")


class FilterModule(object):
    """
    Ansible core jinja2 filters for network configuration management.

    This module provides filters for generating unified diffs, remediation configs,
    and rollback configs for network devices using hier_config.
    """

    def filters(self):
        return {
            "unified_diff": unified_diff_filter,
            "remediation_config": remediation_config_filter,
            "rollback_config": rollback_config_filter,
        }
