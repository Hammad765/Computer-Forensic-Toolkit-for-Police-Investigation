#!/usr/bin/env python3
"""
Computer Forensic Toolkit - Banner and Menu Display
Contains banner and menu display functions
"""

from color import *

def display_banner():
    """Display the welcome banner"""
    print(f"{BRIGHT_GOLD}{BOLD}")
    print(r"""
    ╔═════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                 ║
    ║   ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗   ██╗████████╗███████╗██████╗        ║
    ║  ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗       ║
    ║  ██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║   ██║   █████╗  ██████╔╝       ║
    ║  ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║   ██║   ██║   ██╔══╝  ██╔══██╗       ║
    ║  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ╚██████╔╝   ██║   ███████╗██║  ██║       ║
    ║   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝      ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝       ║
    ║                                                                                 ║
    ║     ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗ ██████╗            ║
    ║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║██╔════╝            ║
    ║     █████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║██║                 ║
    ║     ██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║██║                 ║
    ║     ██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║╚██████╗            ║
    ║     ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝            ║
    ║                                                                                 ║
    ║            ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗            ║
    ║            ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝            ║
    ║               ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║               ║
    ║               ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║               ║
    ║               ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║               ║
    ║               ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝               ║
    ║                                                                                 ║
    ╚═════════════════════════════════════════════════════════════════════════════════╝
    """)
    print(f"{GOLD}{'═' * 85}{RESET}")
    print(f"{ORANGE}{BOLD}        ⚡ Automated Wi-Fi Computer Forensic Investigation Framework ⚡{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}")
    print(f"{GOLD}                  © Copyright Hammad Arshad & Lewis Golightly 2025{RESET}")
    print(f"{GOLD}{'═' * 85}{RESET}\n")

def display_main_menu():
    """Display the main menu options"""
    print(f"\n{GOLD}╔{'═' * 83}╗{RESET}")
    print(f"{GOLD}║{BRIGHT_GOLD}{BOLD}{'CFT CONTROL PANEL':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║{CYAN}{BOLD}{'5 Powerful Attack Modules for WiFi Security Testing':^83}{RESET}{GOLD}║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[1]{GOLD} ⚔️  {ORANGE}Deauthentication Attack{GOLD}     {CYAN}└─ Disconnect clients from target AP{GOLD}       ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[2]{GOLD} 🔐  {ORANGE}WiFi Password Crack{GOLD}         {CYAN}└─ Capture & crack WPA/WPA2 handshake{GOLD}     ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[3]{GOLD} 👥  {ORANGE}Evil Twin Attack{GOLD}            {CYAN}└─ Launch Airgeddon for Evil Twin{GOLD}         ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[4]{GOLD} 💥  {ORANGE}DoS Attack{GOLD}                  {CYAN}└─ Auth/Assoc Flood Attack{GOLD}              ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}║   {BRIGHT_GOLD}[5]{GOLD} 🔑  {ORANGE}Brute Force Password Attack{GOLD} {CYAN}└─ WPS PIN & Password Brute Force{GOLD}       ║{RESET}")
    print(f"{GOLD}║                                                                                   ║{RESET}")
    print(f"{GOLD}╠{'═' * 83}╣{RESET}")
    print(f"{GOLD}║   {RED}[0]{GOLD} 🚪  {RED}Exit Program{GOLD}                                                            ║{RESET}")
    print(f"{GOLD}╚{'═' * 83}╝{RESET}")
