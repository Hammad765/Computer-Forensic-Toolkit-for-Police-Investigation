#!/usr/bin/env python3
"""
QuadStrike - Utility Functions
Contains helper functions used across multiple modules
"""

import subprocess
import os
import re

def check_for_essid(essid, lst):
    """Check if ESSID already exists in the list"""
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False
    return check_status

def list_all_interfaces():
    """
    Returns a list of dicts:
    [{ "name": "eth0", "mac": "aa:bb:...", "is_wireless": True/False }, ...]
    """
    interfaces = []

    # Get interfaces via `ip -o link` (robust)
    try:
        ip_out = subprocess.run(["ip", "-o", "link", "show"], capture_output=True, text=True, check=True).stdout
    except Exception:
        ip_out = ""

    # Parse lines
    for line in ip_out.splitlines():
        m = re.match(r'^\d+:\s+([^:]+):', line)
        if m:
            name = m.group(1)
            if name == "lo":  # skip loopback
                continue
            # get MAC address (if available)
            mac = None
            addr_path = f"/sys/class/net/{name}/address"
            try:
                with open(addr_path) as f:
                    mac = f.read().strip()
            except Exception:
                mac = None

            # Detect wireless: check sysfs wireless dir
            wireless_path = f"/sys/class/net/{name}/wireless"
            is_wireless = os.path.isdir(wireless_path)

            interfaces.append({"name": name, "mac": mac, "is_wireless": is_wireless})

    # If ip didn't return anything, fallback to parsing `iwconfig`
    if len(interfaces) == 0:
        try:
            iwcfg = subprocess.run(["iwconfig"], capture_output=True, text=True, check=True).stdout
            for line in iwcfg.splitlines():
                if not line.strip():
                    continue
                parts = line.split()
                iface = parts[0]
                if iface == "lo":
                    continue
                mac = None
                addr_path = f"/sys/class/net/{iface}/address"
                try:
                    with open(addr_path) as f:
                        mac = f.read().strip()
                except Exception:
                    mac = None
                interfaces.append({"name": iface, "mac": mac, "is_wireless": True})
        except Exception:
            pass

    # Remove duplicates
    seen = set()
    uniq = []
    for i in interfaces:
        if i["name"] not in seen:
            uniq.append(i)
            seen.add(i["name"])
    return uniq
