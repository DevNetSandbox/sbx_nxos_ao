#!/usr/bin/env python
"""
Code sample for use with the DevNet Sandbox Always On Open NX-OS Programmability
"""

from ncclient import manager
import sys
from lxml import etree
import xmltodict



# Set the device variables
DEVICE = "sbx-nxos-mgmt.cisco.com"
USER = 'admin'
PASS = 'Admin_1234!'
PORT = 10000

# create a main() method
def main():
    """
    Main method that adds loopback interface 99 to both the switch.
    """

    loopback_filter = """
    <filter>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <intf-items>
                <lb-items></lb-items>
            </intf-items>
        </System>
    </filter>"""

    ipv4_filter_template = """
    <filter>
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <ipv4-items>
                <inst-items>
                    <dom-items>
                        <Dom-list>
                            <name>default</name>
                            <if-items>
                                <If-list>
                                    <id>{0}</id>
                                </If-list>
                            </if-items>
                        </Dom-list>
                    </dom-items>
                </inst-items>
            </ipv4-items>
        </System>
    </filter>"""



    with manager.connect(host=DEVICE, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         look_for_keys=False, allow_agent=False) as m:

        # Add the loopback interface
        print("\nNow Retrieving Loopback Interfaces from device {}...\n".format(DEVICE))
        netconf_response = m.get(filter=loopback_filter)

        # Read XML results into OrderedDict of Loopbacks
        netconf_data = xmltodict.parse(netconf_response.xml)["rpc-reply"]["data"]

        # See if any loopbacks exist
        try:
            loopbacks = netconf_data["System"]["intf-items"]["lb-items"]["LbRtdIf-list"]
        except KeyError:
            # No Loopbacks configured
            print("There are no Loopback Interfaces Currently Configured.")
            sys.exit()

        # Ensure loopbacks is a list of loopbacks
        # If a single loopback is configured, type will NOT be "list"
        if not type(loopbacks) is list:
            # Create a list with single object
            loopbacks = [loopbacks]

        # Print out details about Loopbacks
        for loopback in loopbacks:
            # Print Basic Loopback details
            print("Interface Id:  {}".format(loopback["id"]))
            print("  Admin State: {}".format(loopback["adminSt"]))
            print("  Oper State:  {}".format(loopback["lbrtdif-items"]["operSt"]))

            # Retrieve IPv4 Address for Loopback
            # Create NETCONF Filter
            ipv4_filter = ipv4_filter_template.format(loopback["id"])

            # Send NETCONF get command
            ipv4_response = m.get(filter=ipv4_filter)

            # Read XML results
            ipv4_data = xmltodict.parse(ipv4_response.xml)["rpc-reply"]["data"]

            # See if IPv4 Addresses exist
            try:
                ipv4_addresses = ipv4_data["System"]["ipv4-items"]["inst-items"]["dom-items"]["Dom-list"]["if-items"]["If-list"]["addr-items"]["Addr-list"]
                # Ensure list of addresses
                if not type(ipv4_addresses) is list:
                    ipv4_addresses = [ipv4_addresses]

                primary_ipv4_address = ipv4_addresses[0]

                # Print IPv4 Address Info
                print("  IPv4 Address: {}".format(primary_ipv4_address["addr"]))
            except KeyError:
                print("  There are no IPv4 addresses configured.")


            # Blank line at end of interface
            print(" ")

if __name__ == '__main__':
    sys.exit(main())
