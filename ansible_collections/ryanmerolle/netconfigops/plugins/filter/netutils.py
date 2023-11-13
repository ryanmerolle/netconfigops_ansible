#!/usr/bin/env python3
from netutils.utils import jinja2_convenience_function

class FilterModule(object):
    """
    Ansible filter module to integrate netutils Jinja2 filters.

    This module provides a convenient way to access all the Jinja2 filters
    available in the netutils package within Ansible templates. These filters
    are useful for various network configuration and parsing tasks.
    """

    def filters(self):
        """
        Returns the Jinja2 filters from the netutils package for use in Ansible.

        This method is called by Ansible to retrieve a dictionary of filter names
        and their corresponding functions provided by the netutils package.

        Returns:
        - dict: A dictionary of Jinja2 filter names and their corresponding functions
          from the netutils package.

        Usage:
        Within an Ansible playbook or role, use these filters in templates as you
        would with any built-in Jinja2 filters. For example, "{{ '192.0.2.1' | ip_to_hex }}"
        to convert an IP address to its hexadecimal representation.
        """
        return jinja2_convenience_function()
