#!/usr/bin/env python3
"""
Computer Forensic Toolkit (CFT) - Main Entry Point
Automated Wi-Fi Computer Forensic Investigation Framework

© Copyright Hammad Arshad & Lewis Golightly 2025

Disclaimer: This script is for educational purposes only. 
Do not use against any network that you don't own or have authorization to test.
"""

import subprocess
import os
import time
import shutil
from datetime import datetime

# Import color codes
from color import *

# Import banner and menu
from banner import display_banner, display_main_menu

# Import attack modules
from deauthentication import deauthentication_attack
from password_cracking import wifi_password_crack
from evil_twin import evil_twin_attack
from dos import dos_attack
from brute_force import brute_force_attack

# Import performance monitor
from performance_monitor import init_monitor, get_monitor
import time as timing_module


def main():
    """Main function - Entry point for Computer Forensic Toolkit"""
    # Check for sudo privileges
    if not 'SUDO_UID' in os.environ.keys():
        print(f"{RED}[✗] This program requires sudo privileges.{RESET}")
        print(f"{GOLD}[i] Please run with: {ORANGE}sudo python3 main.py{RESET}")
        exit()

    # Initialize performance monitor
    print(f"\n{GOLD}[{CYAN}i{GOLD}] Initializing Performance Monitor...{RESET}")
    monitor = init_monitor()
    print(f"{GREEN}[✓] Performance monitoring active!{RESET}\n")
    timing_module.sleep(1)

    # Clean up old CSV files
    for file_name in os.listdir():
        if ".csv" in file_name:
            directory = os.getcwd()
            try:
                os.mkdir(directory + "/backup/")
            except:
                pass
            timestamp = datetime.now()
            shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

    # Display banner once
    subprocess.call("clear", shell=True)
    display_banner()

    # Main menu loop
    while True:
        display_main_menu()
        choice = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Select an option: {ORANGE}")
        print(RESET, end='')

        if choice == "1":
            # Measure latency for module selection
            start_time = timing_module.time()
            
            # Start monitoring CPU and Memory
            monitor.start_monitoring("Deauthentication_Attack")
            
            deauthentication_attack()
            
            # Stop monitoring
            monitor.stop_monitoring()
            
            # Log latency
            duration = timing_module.time() - start_time
            monitor.log_latency("Deauthentication_Attack", "Complete_Workflow", duration)
            
        elif choice == "2":
            start_time = timing_module.time()
            monitor.start_monitoring("WiFi_Password_Crack")
            
            wifi_password_crack()
            
            monitor.stop_monitoring()
            duration = timing_module.time() - start_time
            monitor.log_latency("WiFi_Password_Crack", "Complete_Workflow", duration)
            
        elif choice == "3":
            start_time = timing_module.time()
            monitor.start_monitoring("Evil_Twin_Attack")
            
            evil_twin_attack()
            
            monitor.stop_monitoring()
            duration = timing_module.time() - start_time
            monitor.log_latency("Evil_Twin_Attack", "Complete_Workflow", duration)
            
        elif choice == "4":
            start_time = timing_module.time()
            monitor.start_monitoring("DoS_Attack")
            
            dos_attack()
            
            monitor.stop_monitoring()
            duration = timing_module.time() - start_time
            monitor.log_latency("DoS_Attack", "Complete_Workflow", duration)
            
        elif choice == "5":
            start_time = timing_module.time()
            monitor.start_monitoring("Brute_Force_Attack")
            
            brute_force_attack()
            
            monitor.stop_monitoring()
            duration = timing_module.time() - start_time
            monitor.log_latency("Brute_Force_Attack", "Complete_Workflow", duration)
            
        elif choice == "0":
            # Generate summary before exiting
            print(f"\n{GOLD}[{CYAN}i{GOLD}] Generating performance summary...{RESET}")
            monitor.generate_summary()
            
            print(f"\n{GOLD}[{GREEN}✓{GOLD}] Exiting Computer Forensic Toolkit... Stay safe! {ORANGE}⚡{RESET}\n")
            break
        else:
            print(f"\n{RED}[✗] Invalid option. Please try again.{RESET}")
            timing_module.sleep(1)
            subprocess.call("clear", shell=True)
            display_banner()


if __name__ == "__main__":
    main()
