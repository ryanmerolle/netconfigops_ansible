#!/usr/bin/env python3

DOCUMENTATION = """
    name: nb_inventory
    author:
        - Remy Leone (@sieben)
        - Anthony Ruhier (@Anthony25)
        - Nikhil Singh Baliyan (@nikkytub)
        - Sander Steffann (@steffann)
        - Douglas Heriot (@DouglasHeriot)
    short_description: NetBox inventory source
    description:
        - Get inventory hosts from NetBox
    extends_documentation_fragment:
        - constructed
        - inventory_cache
    options:
        plugin:
            description: token that ensures this is a source file for the 'netbox' plugin.
            required: True
            choices: ['netbox.netbox.nb_inventory']
        api_endpoint:
            description: Endpoint of the NetBox API
            required: True
            env:
                - name: NETBOX_API
        validate_certs:
            description:
                - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
            default: True
            type: boolean
        cert:
            description:
                - Certificate path
            default: False
        key:
            description:
                - Certificate key path
            default: False
        ca_path:
            description:
                - CA path
            default: False
        follow_redirects:
            description:
                - Determine how redirects are followed.
                - By default, I(follow_redirects) is set to uses urllib2 default behavior.
            default: urllib2
            choices: ['urllib2', 'all', 'yes', 'safe', 'none']
        config_context:
            description:
                - If True, it adds config_context in host vars.
                - Config-context enables the association of arbitrary data to devices and virtual machines grouped by
                  region, site, role, platform, and/or tenant. Please check official netbox docs for more info.
            default: False
            type: boolean
        flatten_config_context:
            description:
                - If I(config_context) is enabled, by default it's added as a host var named config_context.
                - If flatten_config_context is set to True, the config context variables will be added directly to the host instead.
            default: False
            type: boolean
            version_added: "0.2.1"
        flatten_local_context_data:
            description:
                - If I(local_context_data) is enabled, by default it's added as a host var named local_context_data.
                - If flatten_local_context_data is set to True, the config context variables will be added directly to the host instead.
            default: False
            type: boolean
            version_added: "0.3.0"
        flatten_custom_fields:
            description:
                - By default, host custom fields are added as a dictionary host var named custom_fields.
                - If flatten_custom_fields is set to True, the fields will be added directly to the host instead.
            default: False
            type: boolean
            version_added: "0.2.1"
        token:
            required: False
            description:
                - NetBox API token to be able to read against NetBox.
                - This may not be required depending on the NetBox setup.
                - You can provide a "type" and "value" for a token if your NetBox deployment is using a more advanced authentication like OAUTH.
                - If you do not provide a "type" and "value" parameter, the HTTP authorization header will be set to "Token", which is the NetBox default
            env:
                # in order of precedence
                - name: NETBOX_TOKEN
                - name: NETBOX_API_KEY
        plurals:
            description:
                - If True, all host vars are contained inside single-element arrays for legacy compatibility with old versions of this plugin.
                - Group names will be plural (ie. "sites_mysite" instead of "site_mysite")
                - The choices of I(group_by) will be changed by this option.
            default: True
            type: boolean
            version_added: "0.2.1"
        interfaces:
            description:
                - If True, it adds the device or virtual machine interface information in host vars.
            default: False
            type: boolean
            version_added: "0.1.7"
        site_data:
            description:
                - If True, sites' full data structures returned from Netbox API are included in host vars.
            default: False
            type: boolean
            version_added: "3.5.0"
        prefixes:
            description:
                - If True, it adds the device or virtual machine prefixes to hostvars nested under "site".
                - Must match selection for "site_data", as this changes the structure of "site" in hostvars
            default: False
            type: boolean
            version_added: "3.5.0"
        services:
            description:
                - If True, it adds the device or virtual machine services information in host vars.
            default: True
            type: boolean
            version_added: "0.2.0"
        fetch_all:
            description:
                - By default, fetching interfaces and services will get all of the contents of NetBox regardless of query_filters applied to devices and VMs.
                - When set to False, separate requests will be made fetching interfaces, services, and IP addresses for each device_id and virtual_machine_id.
                - If you are using the various query_filters options to reduce the number of devices, you may find querying NetBox faster with fetch_all set to False.
                - For efficiency, when False, these requests will be batched, for example /api/dcim/interfaces?limit=0&device_id=1&device_id=2&device_id=3
                - These GET request URIs can become quite large for a large number of devices. If you run into HTTP 414 errors, you can adjust the max_uri_length option to suit your web server.
            default: True
            type: boolean
            version_added: "0.2.1"
        group_by:
            description:
                - Keys used to create groups. The I(plurals) and I(racks) options control which of these are valid.
                - I(rack_group) is supported on NetBox versions 2.10 or lower only
                - I(location) is supported on NetBox versions 2.11 or higher only
            type: list
            elements: str
            choices:
                - sites
                - site
                - location
                - tenants
                - tenant
                - racks
                - rack
                - rack_group
                - rack_role
                - tags
                - tag
                - device_roles
                - role
                - device_types
                - device_type
                - manufacturers
                - manufacturer
                - platforms
                - platform
                - region
                - site_group
                - cluster
                - cluster_type
                - cluster_group
                - is_virtual
                - services
                - status
                - time_zone
                - utc_offset
            default: []
        group_names_raw:
            description: Will not add the group_by choice name to the group names
            default: False
            type: boolean
            version_added: "0.2.0"
        query_filters:
            description:
                - List of parameters passed to the query string for both devices and VMs (Multiple values may be separated by commas).
                - You can also use Jinja2 templates.
            type: list
            elements: str
            default: []
        device_query_filters:
            description:
                - List of parameters passed to the query string for devices (Multiple values may be separated by commas).
                - You can also use Jinja2 templates.
            type: list
            elements: str
            default: []
        vm_query_filters:
            description:
                - List of parameters passed to the query string for VMs (Multiple values may be separated by commas).
                - You can also use Jinja2 templates.
            type: list
            elements: str
            default: []
        timeout:
            description: Timeout for NetBox requests in seconds
            type: int
            default: 60
        max_uri_length:
            description:
                - When fetch_all is False, GET requests to NetBox may become quite long and return a HTTP 414 (URI Too Long).
                - You can adjust this option to be smaller to avoid 414 errors, or larger for a reduced number of requests.
            type: int
            default: 4000
            version_added: "0.2.1"
        virtual_chassis_name:
            description:
                - When a device is part of a virtual chassis, use the virtual chassis name as the Ansible inventory hostname.
                - The host var values will be from the virtual chassis master.
            type: boolean
            default: False
        dns_name:
            description:
                - Force IP Addresses to be fetched so that the dns_name for the primary_ip of each device or VM is set as a host_var.
                - Setting interfaces will also fetch IP addresses and the dns_name host_var will be set.
            type: boolean
            default: False
        ansible_host_dns_name:
            description:
                - If True, sets DNS Name (fetched from primary_ip) to be used in ansible_host variable, instead of IP Address.
            type: boolean
            default: False
        compose:
            description: List of custom ansible host vars to create from the device object fetched from NetBox
            default: {}
            type: dict
        racks:
            description:
                - If False, skip querying the racks for information, which can be slow with great amounts of racks.
                - The choices of I(group_by) will be changed by this option.
            type: boolean
            default: True
            version_added: "3.6.0"
"""

EXAMPLES = """
# netbox_inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i netbox_inventory.yml

plugin: netbox.netbox.nb_inventory
api_endpoint: http://localhost:8000
validate_certs: True
config_context: False
group_by:
  - device_roles
query_filters:
  - role: network-edge-router
device_query_filters:
  - has_primary_ip: 'true'
  - tenant__n: internal

# has_primary_ip is a useful way to filter out patch panels and other passive devices
# Adding '__n' to a field searches for the negation of the value.
# The above searches for devices that are NOT "tenant = internal"

# Query filters are passed directly as an argument to the fetching queries.
# You can repeat tags in the query string.

query_filters:
  - role: server
  - tag: web
  - tag: production

# See the NetBox documentation at https://netbox.readthedocs.io/en/stable/rest-api/overview/
# the query_filters work as a logical **OR**
#
# Prefix any custom fields with cf_ and pass the field value with the regular NetBox query string

query_filters:
  - cf_foo: bar

# NetBox inventory plugin also supports Constructable semantics
# You can fill your hosts vars using the compose option:

plugin: netbox.netbox.nb_inventory
compose:
  foo: last_updated
  bar: display_name
  nested_variable: rack.display_name

# You can use keyed_groups to group on properties of devices or VMs.
# NOTE: It's only possible to key off direct items on the device/VM objects.
plugin: netbox.netbox.nb_inventory
keyed_groups:
  - prefix: status
    key: status.value

# For use in Ansible Tower (AWX), please see this blog from RedHat: https://www.ansible.com/blog/using-an-inventory-plugin-from-a-collection-in-ansible-tower
# The credential for NetBox will need to expose NETBOX_API and NETBOX_TOKEN as environment variables.
# Example Ansible Tower credential Input Configuration:

fields:
  - id: NETBOX_API
    type: string
    label: NetBox Host URL
  - id: NETBOX_TOKEN
    type: string
    label: NetBox API Token
    secret: true
required:
  - NETBOX_API
  - NETBOX_TOKEN

# Example Ansible Tower credential Injector Configuration:

env:
  NETBOX_API: '{{ NETBOX_API }}'
  NETBOX_TOKEN: '{{ NETBOX_TOKEN }}'

# Example of time_zone and utc_offset usage

plugin: netbox.netbox.nb_inventory
api_endpoint: http://localhost:8000
token: <insert token>
validate_certs: True
config_context: True
group_by:
  - site
  - role
  - time_zone
  - utc_offset
device_query_filters:
  - has_primary_ip: 'true'
  - manufacturer_id: 1

# using group by time_zone, utc_offset it will group devices in ansible groups depending on time zone configured on site.
# time_zone gives grouping like:
# - "time_zone_Europe_Bucharest"
# - "time_zone_Europe_Copenhagen"
# - "time_zone_America_Denver"
# utc_offset gives grouping like:
# - "time_zone_utc_minus_7"
# - "time_zone_utc_plus_1"
# - "time_zone_utc_plus_10"

# Example of using a token type

plugin: netbox.netbox.nb_inventory
api_endpoint: http://localhost:8000
token:
  type: Bearer
  value: test123456
"""

from ansible.errors import AnsibleFilterError
from hier_config import Host


def load_host_configs(running_config_text, generated_config_text):
    """
    Used by the filter functions. Creates a Host object and loads running and generated configuration texts.
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
        remediation_config = host.remediation_config_filtered_text(
            include_tags={}, exclude_tags={}
        )
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
