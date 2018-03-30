# Open NX-OS Sandbox Model Driven Programmability Samples 

In this folder are several examples scripts for working with Open NX-OS using Model Driven Programmability and Python.  

## Prereqs

To run these scripts you'll need Python 3.6.2+ or Python 2.7.14+ installed on your workstation.  You'll also need to install the `ncclient` library for making NETCONF connections to the sandbox.  

```bash
# Verify Python Version
python -V

Python 3.6.3

# Install ncclient
pip install ncclient
```

For connivence a `requirements.txt` file is included in the repo.  

```bash
pip install -r requirements.txt
```

## Scripts

The following scripts are included.  

* `get_capabilities.py` - Connect to device, say `<hello>` and print capabilities list.
* `get_serial.py` - Send a `<get-config>` operation to retrieve the Serial Number.
* `get_loopbacks.py` - Query the device for any Loopbacks configured and print the details.
* `add_loopback_full.py` - Add a new Loopback to the device.
* `delete_loopback.py` - Delete a Loopback from the device.
