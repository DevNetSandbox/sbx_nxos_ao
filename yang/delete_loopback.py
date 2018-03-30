#!/usr/bin/env python
"""
Code sample for use with the DevNet Sandbox Always On Open NX-OS Programmability
"""

from ncclient import manager
import sys
from lxml import etree


# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

# Ask user for loopback to configure
loopback_number = input("What Loopback interface should be removed? (Provide Id Number Only)\n")

# Verify input
try:
    int(loopback_number)
except ValueError:
    print("Error: Provide just the interface number.  Example 101")
    sys.exit()

LOOPBACK = {'loopback': 'lo{}'.format(loopback_number),
               'name': 'Loopback{}'.format(loopback_number)
              }


# create a main() method
def main():
    """
    Main method that adds loopback interfaces and configures an IP address to
    both the spine switches.
    """

    remove_ip_interface = """<config>
    <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <intf-items>
        <lb-items>
            <LbRtdIf-list operation="delete">
                <id>{0}</id>
            </LbRtdIf-list>
        </lb-items>
    </intf-items>
</System>
</config>"""


    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # Add the loopback interface
        print("\nNow removing intf {} from device {}...\n".format(
                        LOOPBACK['name'],
                        DEVICE)
                        )

        data = remove_ip_interface.format(LOOPBACK['loopback'])

        netconf_response = m.edit_config(target='running', config=data)
        # Parse the XML response
        print(netconf_response)


if __name__ == '__main__':
    sys.exit(main())
