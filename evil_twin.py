#!/usr/bin/env python3
"""
QuadStrike - Evil Twin Attack Module
Launches Airgeddon for Evil Twin attacks
"""

import subprocess
from color import *

def evil_twin_attack():
    """Evil Twin attack module - Launch Airgeddon"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{ORANGE}{BOLD}{'👥  EVIL TWIN ATTACK MODULE  👥':^92}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] This module will launch Airgeddon - a multi-use WiFi security tool{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Airgeddon provides Evil Twin attack and various other options{RESET}")
    
    # Check if airgeddon is installed
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Checking if Airgeddon is installed...{RESET}")
    
    airgeddon_check = subprocess.run(["which", "airgeddon"], capture_output=True, text=True)
    
    if airgeddon_check.returncode != 0:
        print(f"\n{RED}[✗] Airgeddon is not installed on this system.{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] To install Airgeddon:{RESET}")
        print(f"{GOLD}    1. Clone the repository: {ORANGE}git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git{RESET}")
        print(f"{GOLD}    2. Navigate to directory: {ORANGE}cd airgeddon{RESET}")
        print(f"{GOLD}    3. Run: {ORANGE}sudo bash airgeddon.sh{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] Or check: {ORANGE}https://github.com/v1s1t0r1sh3r3/airgeddon{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return
    
    print(f"{GOLD}[{GREEN}✓{GOLD}] Airgeddon found!{RESET}")
    
    # Display information
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'LAUNCHING AIRGEDDON':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║  Airgeddon is a comprehensive WiFi security auditing tool                         ║{RESET}")
    print(f"{GOLD}║  It includes multiple attack modes including:                                     ║{RESET}")
    print(f"{GOLD}║    • Evil Twin attacks (Captive Portal)                                           ║{RESET}")
    print(f"{GOLD}║    • DoS attacks (various methods)                                                ║{RESET}")
    print(f"{GOLD}║    • WPS attacks                                                                  ║{RESET}")
    print(f"{GOLD}║    • WPA/WPA2 handshake capture and cracking                                      ║{RESET}")
    print(f"{GOLD}║    • And much more...                                                             ║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{ORANGE}⚠{GOLD}] Use only on networks you own or have authorization to test!{RESET}")
    
    confirm = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Launch Airgeddon? (y/n): {ORANGE}")
    print(RESET, end='')
    
    if confirm.lower() != 'y':
        print(f"\n{ORANGE}[!] Cancelled.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return
    
    print(f"\n{GOLD}[{GREEN}+{GOLD}] Launching Airgeddon...{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Airgeddon will open in a new window or session{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] When you exit Airgeddon, you will return to this menu{RESET}\n")
    
    # Launch airgeddon as root
    try:
        subprocess.run(["sudo", "airgeddon"])
        
        # Display success message when airgeddon closes normally
        print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
        print(f"{GOLD}║{GREEN}{BOLD}{'EVIL TWIN ATTACK SESSION COMPLETED':^83}{RESET}{GOLD}║{RESET}")
        print(f"{GOLD}╚{'═' * 83}╝{RESET}")
        
        print(f"\n{GREEN}[✓] Airgeddon session completed successfully!{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] All attacks and operations have been closed{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Check Airgeddon's output for any captured credentials{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n\n{GOLD}[{ORANGE}!{GOLD}] Airgeddon interrupted{RESET}")
    except Exception as e:
        print(f"\n{RED}[✗] Error launching Airgeddon: {str(e)}{RESET}")
    
    print(f"\n{GOLD}[{GREEN}✓{GOLD}] Airgeddon closed.{RESET}")
    input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
