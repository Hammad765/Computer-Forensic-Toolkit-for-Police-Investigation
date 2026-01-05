#!/usr/bin/env python3
"""
Computer Forensic Toolkit - Brute Force Attack Module
Performs WPS PIN brute force and password dictionary attacks
"""

import subprocess
import csv
import os
import time
from color import *
from utils import list_all_interfaces, check_for_essid
from password_cracking import wifi_password_crack

def display_cracked_password(output_file):
    """Display cracked password using hashcat --show"""
    print(f"\n{GOLD}{'═' * 85}{RESET}")
    print(f"{CYAN}[i] Retrieving cracked password...{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}\n")
    
    try:
        show_result = subprocess.run(
            ["hashcat", "-m", "22000", output_file, "--show"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if show_result.returncode == 0 and show_result.stdout.strip():
            print(f"{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{GREEN}{BOLD}{'CRACKED PASSWORD':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}\n")
            print(f"{GREEN}{BOLD}{show_result.stdout.strip()}{RESET}\n")
            print(f"{GOLD}[{GREEN}✓{GOLD}] Password successfully cracked!{RESET}")
        else:
            print(f"{ORANGE}[!] No cracked passwords found in hashcat.potfile{RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] The password may not be in the 8-digit numeric range.{RESET}")
    
    except Exception as e:
        print(f"{ORANGE}[!] Could not retrieve cracked password: {str(e)}{RESET}")

def brute_force_attack():
    """Brute Force Password Attack module - Crack WiFi passwords"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{ORANGE}{BOLD}{'🔑  BRUTE FORCE PASSWORD ATTACK  🔑':^92}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] This module cracks WiFi passwords using captured handshakes{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] You can use an existing .cap file or capture a new handshake{RESET}")
    
    # Display options
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'SELECT AN OPTION':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[1]{GOLD} ➤  {ORANGE}Enter .cap file location{GOLD}      {CYAN}└─ Use existing handshake file{GOLD}       ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[2]{GOLD} ➤  {ORANGE}Don't have .cap file?{GOLD}         {CYAN}└─ Capture handshake now{GOLD}            ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {RED}[0]{GOLD} ➤  {RED}Return to Main Menu{GOLD}                                                     ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    choice = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Select an option: {ORANGE}")
    print(RESET, end='')
    
    if choice == "1":
        # Option 1: Enter existing .cap file location
        use_existing_cap_file()
    elif choice == "2":
        # Option 2: Capture new handshake
        capture_new_handshake()
    elif choice == "0":
        return
    else:
        print(f"\n{RED}[✗] Invalid option.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")

def use_existing_cap_file():
    """Use an existing .cap file for password cracking"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'USE EXISTING .CAP FILE':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    # Ask for .cap file location
    cap_file = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Enter the path to your .cap file: {ORANGE}")
    print(RESET, end='')
    
    # Check if file exists
    if not os.path.exists(cap_file):
        print(f"\n{RED}[✗] File not found: {cap_file}{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Please check the file path and try again.{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
    
    # Check if it's a .cap file
    if not cap_file.endswith('.cap'):
        print(f"\n{ORANGE}[!] Warning: File doesn't have .cap extension{RESET}")
        confirm = input(f"{GOLD}[{BRIGHT_GOLD}?{GOLD}] Continue anyway? (y/n): {ORANGE}")
        print(RESET, end='')
        if confirm.lower() != 'y':
            return
    
    print(f"\n{GOLD}[{GREEN}✓{GOLD}] File found: {ORANGE}{cap_file}{RESET}")
    
    # Display file info
    try:
        file_size = os.path.getsize(cap_file)
        file_size_kb = file_size / 1024
        print(f"{GOLD}[{CYAN}i{GOLD}] File size: {file_size_kb:.2f} KB{RESET}")
    except:
        pass
    
    # Convert .cap to .22000 format
    print(f"\n{GOLD}{'═' * 85}{RESET}")
    print(f"{CYAN}[i] Converting .cap file to .22000 format for hashcat...{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}")
    
    # Generate output filename (remove .cap and add .22000)
    base_name = cap_file.rsplit('.', 1)[0]
    output_file = f"{base_name}.22000"
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] Running conversion: hcxpcapngtool{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Input:  {ORANGE}{cap_file}{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Output: {ORANGE}{output_file}{RESET}")
    
    try:
        # Run hcxpcapngtool to convert .cap to .22000
        result = subprocess.run(
            ["hcxpcapngtool", cap_file, "-o", output_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check if conversion was successful
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"\n{GOLD}[{GREEN}✓{GOLD}] Conversion successful!{RESET}")
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{GREEN}{BOLD}{'CONVERTED FILE DETAILS':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            # Display converted file details
            try:
                converted_size = os.path.getsize(output_file)
                converted_size_kb = converted_size / 1024
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Converted file: {GREEN}{output_file}{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] File size: {converted_size_kb:.2f} KB{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Format: .22000 (hashcat compatible){RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Location: {os.path.dirname(os.path.abspath(output_file)) or 'Current directory'}{RESET}")
            except Exception as e:
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Converted file: {GREEN}{output_file}{RESET}")
            
            print(f"\n{CYAN}[i] File is ready for password cracking with hashcat!{RESET}")
            
            # Ask user if they want to proceed with hashcat
            print(f"\n{GOLD}{'═' * 85}{RESET}")
            proceed_crack = input(f"{GOLD}[{BRIGHT_GOLD}?{GOLD}] Do you want to start hashcat brute force attack now? (y/n): {ORANGE}")
            print(RESET, end='')
            
            if proceed_crack.lower() != 'y':
                print(f"\n{ORANGE}[!] Password cracking cancelled.{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Converted file saved: {GREEN}{output_file}{RESET}")
                input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
                return
            
            # Launch hashcat brute force attack
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{ORANGE}{BOLD}{'HASHCAT BRUTE FORCE ATTACK':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            print(f"\n{GOLD}[{CYAN}i{GOLD}] Attack Mode: Brute Force (Mask Attack){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Hash Type: WPA-PBKDF2-PMKID+EAPOL (22000){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Mask: ?d?d?d?d?d?d?d?d (8-digit numeric password){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Target: {ORANGE}{output_file}{RESET}")
            
            print(f"\n{CYAN}[i] Starting hashcat brute force attack...{RESET}")
            print(f"{CYAN}[i] This may take a while depending on your hardware.{RESET}")
            print(f"{CYAN}[i] Press {RED}Ctrl+C{CYAN} to stop the attack.{RESET}\n")
            
            print(f"{GOLD}{'═' * 85}{RESET}")
            
            try:
                # Run hashcat brute force attack
                # -a 3 = Brute force (mask attack)
                # -m 22000 = WPA-PBKDF2-PMKID+EAPOL
                # ?d?d?d?d?d?d?d?d = 8 digit numeric password
                result = subprocess.run(
                    ["hashcat", "-a", "3", "-m", "22000", output_file, "?d?d?d?d?d?d?d?d"],
                    capture_output=False,
                    text=True
                )
                
                print(f"\n{GOLD}{'═' * 85}{RESET}")
                
                if result.returncode == 0:
                    print(f"\n{GREEN}[✓] Hashcat attack completed!{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] Check the output above for cracked passwords.{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] Cracked passwords are also saved in hashcat.potfile{RESET}")
                    
                    # Display the cracked password using --show
                    display_cracked_password(output_file)
                    
                else:
                    print(f"\n{ORANGE}[!] Hashcat finished with status code: {result.returncode}{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] The password may not have been found.{RESET}")
                
            except KeyboardInterrupt:
                print(f"\n\n{GOLD}[{GREEN}✓{GOLD}] Hashcat attack stopped by user.{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Partial results (if any) are saved in hashcat.potfile{RESET}")
                
            except FileNotFoundError:
                print(f"\n{RED}[✗] Hashcat not found!{RESET}")
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Hashcat is required for password cracking{RESET}")
                print(f"\n{ORANGE}[!] Installation instructions:{RESET}")
                print(f"{CYAN}    sudo apt-get update{RESET}")
                print(f"{CYAN}    sudo apt-get install hashcat{RESET}")
                
            except Exception as e:
                print(f"\n{RED}[✗] An error occurred during hashcat attack: {str(e)}{RESET}")
            
            input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
            return
            
        else:
            # Conversion failed
            print(f"\n{RED}[✗] Conversion failed!{RESET}")
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{RED}{BOLD}{'CONVERSION ERROR':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            print(f"\n{RED}[✗] Failed to convert {cap_file} to .22000 format{RESET}")
            print(f"\n{GOLD}[{CYAN}i{GOLD}] Possible reasons:{RESET}")
            print(f"{GOLD}    • hcxpcapngtool is not installed{RESET}")
            print(f"{GOLD}    • The .cap file doesn't contain valid handshake data{RESET}")
            print(f"{GOLD}    • The .cap file is corrupted{RESET}")
            print(f"{GOLD}    • Insufficient permissions{RESET}")
            
            if result.stderr:
                print(f"\n{GOLD}[{RED}!{GOLD}] Error details:{RESET}")
                print(f"{RED}{result.stderr[:500]}{RESET}")
            
            print(f"\n{ORANGE}[!] To install hcxpcapngtool:{RESET}")
            print(f"{CYAN}    sudo apt-get install hcxtools{RESET}")
            
            input(f"\n{GOLD}Press Enter to return...{RESET}")
            return
            
    except FileNotFoundError:
        print(f"\n{RED}[✗] hcxpcapngtool not found!{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] hcxpcapngtool is required to convert .cap files{RESET}")
        print(f"\n{ORANGE}[!] Installation instructions:{RESET}")
        print(f"{CYAN}    sudo apt-get update{RESET}")
        print(f"{CYAN}    sudo apt-get install hcxtools{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
        
    except subprocess.TimeoutExpired:
        print(f"\n{RED}[✗] Conversion timed out!{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] The conversion process took too long.{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
        
    except Exception as e:
        print(f"\n{RED}[✗] An error occurred during conversion: {str(e)}{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return

def capture_new_handshake():
    """Capture a new handshake for password cracking"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'CAPTURE NEW HANDSHAKE':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] This will launch the handshake capture process{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] The WiFi Password Crack module will be used to capture the handshake{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Once captured, you'll need to provide the .cap file location{RESET}")
    
    proceed = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Ready to start? (y/n): {ORANGE}")
    print(RESET, end='')
    
    if proceed.lower() != 'y':
        print(f"\n{ORANGE}[!] Handshake capture cancelled.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return
    
    print(f"\n{GOLD}{'═' * 85}{RESET}")
    print(f"{CYAN}[i] Launching WiFi Password Crack module for handshake capture...{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}\n")
    
    # Call the WiFi Password Crack function (Option 2)
    # This will perform the entire handshake capture process
    wifi_password_crack()
    
    # After handshake capture is complete, ask for the .cap file location
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'HANDSHAKE CAPTURE COMPLETE':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
    
    print(f"\n{GOLD}[{GREEN}✓{GOLD}] Handshake capture process finished!{RESET}")
    print(f"\n{CYAN}[i] Now you need to provide the location of the captured .cap file{RESET}")
    print(f"{CYAN}[i] The file was saved during the capture process{RESET}")
    print(f"{CYAN}[i] It should be in the current directory with a name like: filename-01.cap{RESET}")
    
    # Ask for .cap file location
    cap_file = input(f"\n{GOLD}[{BRIGHT_GOLD}?{GOLD}] Enter the path to the captured .cap file: {ORANGE}")
    print(RESET, end='')
    
    # Check if file exists
    if not os.path.exists(cap_file):
        print(f"\n{RED}[✗] File not found: {cap_file}{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] Please check the file path and try again.{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] The file should be in your current directory.{RESET}")
        input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
        return
    
    # Check if it's a .cap file
    if not cap_file.endswith('.cap'):
        print(f"\n{ORANGE}[!] Warning: File doesn't have .cap extension{RESET}")
        confirm = input(f"{GOLD}[{BRIGHT_GOLD}?{GOLD}] Continue anyway? (y/n): {ORANGE}")
        print(RESET, end='')
        if confirm.lower() != 'y':
            return
    
    print(f"\n{GOLD}[{GREEN}✓{GOLD}] File found: {ORANGE}{cap_file}{RESET}")
    
    # Display file info
    try:
        file_size = os.path.getsize(cap_file)
        file_size_kb = file_size / 1024
        print(f"{GOLD}[{CYAN}i{GOLD}] File size: {file_size_kb:.2f} KB{RESET}")
    except:
        pass
    
    # Convert .cap to .22000 format
    print(f"\n{GOLD}{'═' * 85}{RESET}")
    print(f"{CYAN}[i] Converting .cap file to .22000 format for hashcat...{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}")
    
    # Generate output filename (remove .cap and add .22000)
    base_name = cap_file.rsplit('.', 1)[0]
    output_file = f"{base_name}.22000"
    
    print(f"\n{GOLD}[{CYAN}i{GOLD}] Running conversion: hcxpcapngtool{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Input:  {ORANGE}{cap_file}{RESET}")
    print(f"{GOLD}[{CYAN}i{GOLD}] Output: {ORANGE}{output_file}{RESET}")
    
    try:
        # Run hcxpcapngtool to convert .cap to .22000
        result = subprocess.run(
            ["hcxpcapngtool", cap_file, "-o", output_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check if conversion was successful
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"\n{GOLD}[{GREEN}✓{GOLD}] Conversion successful!{RESET}")
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{GREEN}{BOLD}{'CONVERTED FILE DETAILS':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            # Display converted file details
            try:
                converted_size = os.path.getsize(output_file)
                converted_size_kb = converted_size / 1024
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Converted file: {GREEN}{output_file}{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] File size: {converted_size_kb:.2f} KB{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Format: .22000 (hashcat compatible){RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Location: {os.path.dirname(os.path.abspath(output_file)) or 'Current directory'}{RESET}")
            except Exception as e:
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Converted file: {GREEN}{output_file}{RESET}")
            
            print(f"\n{CYAN}[i] File is ready for password cracking with hashcat!{RESET}")
            
            # Ask user if they want to proceed with hashcat
            print(f"\n{GOLD}{'═' * 85}{RESET}")
            proceed_crack = input(f"{GOLD}[{BRIGHT_GOLD}?{GOLD}] Do you want to start hashcat brute force attack now? (y/n): {ORANGE}")
            print(RESET, end='')
            
            if proceed_crack.lower() != 'y':
                print(f"\n{ORANGE}[!] Password cracking cancelled.{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Converted file saved: {GREEN}{output_file}{RESET}")
                input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
                return
            
            # Launch hashcat brute force attack
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{ORANGE}{BOLD}{'HASHCAT BRUTE FORCE ATTACK':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            print(f"\n{GOLD}[{CYAN}i{GOLD}] Attack Mode: Brute Force (Mask Attack){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Hash Type: WPA-PBKDF2-PMKID+EAPOL (22000){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Mask: ?d?d?d?d?d?d?d?d (8-digit numeric password){RESET}")
            print(f"{GOLD}[{CYAN}i{GOLD}] Target: {ORANGE}{output_file}{RESET}")
            
            print(f"\n{CYAN}[i] Starting hashcat brute force attack...{RESET}")
            print(f"{CYAN}[i] This may take a while depending on your hardware.{RESET}")
            print(f"{CYAN}[i] Press {RED}Ctrl+C{CYAN} to stop the attack.{RESET}\n")
            
            print(f"{GOLD}{'═' * 85}{RESET}")
            
            try:
                # Run hashcat brute force attack
                # -a 3 = Brute force (mask attack)
                # -m 22000 = WPA-PBKDF2-PMKID+EAPOL
                # ?d?d?d?d?d?d?d?d = 8 digit numeric password
                result = subprocess.run(
                    ["hashcat", "-a", "3", "-m", "22000", output_file, "?d?d?d?d?d?d?d?d"],
                    capture_output=False,
                    text=True
                )
                
                print(f"\n{GOLD}{'═' * 85}{RESET}")
                
                if result.returncode == 0:
                    print(f"\n{GREEN}[✓] Hashcat attack completed!{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] Check the output above for cracked passwords.{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] Cracked passwords are also saved in hashcat.potfile{RESET}")
                    
                    # Display the cracked password using --show
                    display_cracked_password(output_file)
                    
                else:
                    print(f"\n{ORANGE}[!] Hashcat finished with status code: {result.returncode}{RESET}")
                    print(f"{GOLD}[{CYAN}i{GOLD}] The password may not have been found.{RESET}")
                
            except KeyboardInterrupt:
                print(f"\n\n{GOLD}[{GREEN}✓{GOLD}] Hashcat attack stopped by user.{RESET}")
                print(f"{GOLD}[{CYAN}i{GOLD}] Partial results (if any) are saved in hashcat.potfile{RESET}")
                
            except FileNotFoundError:
                print(f"\n{RED}[✗] Hashcat not found!{RESET}")
                print(f"\n{GOLD}[{CYAN}i{GOLD}] Hashcat is required for password cracking{RESET}")
                print(f"\n{ORANGE}[!] Installation instructions:{RESET}")
                print(f"{CYAN}    sudo apt-get update{RESET}")
                print(f"{CYAN}    sudo apt-get install hashcat{RESET}")
                
            except Exception as e:
                print(f"\n{RED}[✗] An error occurred during hashcat attack: {str(e)}{RESET}")
            
            input(f"\n{GOLD}Press Enter to return to main menu...{RESET}")
            return
            
        else:
            # Conversion failed
            print(f"\n{RED}[✗] Conversion failed!{RESET}")
            print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
            print(f"{GOLD}║{RED}{BOLD}{'CONVERSION ERROR':^83}{RESET}{GOLD}║{RESET}")
            print(f"{GOLD}╚{'═' * 83}╝{RESET}")
            
            print(f"\n{RED}[✗] Failed to convert {cap_file} to .22000 format{RESET}")
            print(f"\n{GOLD}[{CYAN}i{GOLD}] Possible reasons:{RESET}")
            print(f"{GOLD}    • hcxpcapngtool is not installed{RESET}")
            print(f"{GOLD}    • The .cap file doesn't contain valid handshake data{RESET}")
            print(f"{GOLD}    • The .cap file is corrupted{RESET}")
            print(f"{GOLD}    • Insufficient permissions{RESET}")
            
            if result.stderr:
                print(f"\n{GOLD}[{RED}!{GOLD}] Error details:{RESET}")
                print(f"{RED}{result.stderr[:500]}{RESET}")
            
            print(f"\n{ORANGE}[!] To install hcxpcapngtool:{RESET}")
            print(f"{CYAN}    sudo apt-get install hcxtools{RESET}")
            
            input(f"\n{GOLD}Press Enter to return...{RESET}")
            return
            
    except FileNotFoundError:
        print(f"\n{RED}[✗] hcxpcapngtool not found!{RESET}")
        print(f"\n{GOLD}[{CYAN}i{GOLD}] hcxpcapngtool is required to convert .cap files{RESET}")
        print(f"\n{ORANGE}[!] Installation instructions:{RESET}")
        print(f"{CYAN}    sudo apt-get update{RESET}")
        print(f"{CYAN}    sudo apt-get install hcxtools{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
        
    except subprocess.TimeoutExpired:
        print(f"\n{RED}[✗] Conversion timed out!{RESET}")
        print(f"{GOLD}[{CYAN}i{GOLD}] The conversion process took too long.{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
        
    except Exception as e:
        print(f"\n{RED}[✗] An error occurred during conversion: {str(e)}{RESET}")
        input(f"\n{GOLD}Press Enter to return...{RESET}")
        return
