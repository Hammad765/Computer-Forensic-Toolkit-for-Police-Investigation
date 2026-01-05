# Computer Forensic Toolkit for Police Investigation

Automated wireless network forensic analysis toolkit integrating five attack vectors for law enforcement investigations.

## 🎓 Academic Project

**Institution:** Teesside University  
**Program:** MSc Cyber Security (with Advanced Practice)  
**Author:** Hammad Arshad (Student ID: D3261969)  
**Supervisors:** Mr. Lewis Golightly, Dr. Qiang Guo  
**Date:** January 2026

## 📋 Overview

This toolkit consolidates five wireless attack vectors into a unified forensic platform:

1. **Deauthentication Attack** - Force client disconnection for handshake capture
2. **Dictionary Attack** - WPA2 password recovery using rockyou.txt wordlist
3. **Evil Twin Attack** - Rogue access point with captive portal credential capture
4. **DoS Authentication Flood** - Access point resource exhaustion via spoofed frames
5. **Hashcat Brute-Force** - GPU-accelerated password cracking

## 🔧 Features

- ✅ Automated attack execution with menu-driven interface
- ✅ Real-time performance monitoring (CPU, memory, latency)
- ✅ Forensic evidence collection with chain-of-custody metadata
- ✅ Timestamped logging for court admissibility
- ✅ Packet capture preservation (.cap/.pcap format)
- ✅ Automated report generation

## 🖥️ System Requirements

**Operating System:**
- Kali Linux 2024.x (recommended)
- Ubuntu 22.04+ (supported)

**Hardware:**
- Wireless adapter with monitor mode and packet injection support
  - Recommended: Atheros AR9271, Realtek RTL8812AU
- Minimum 8GB RAM
- Multi-core CPU (Intel i5 or equivalent)
- Optional: NVIDIA/AMD GPU for Hashcat acceleration

**Software Dependencies:**
- Python 3.10+
- Aircrack-ng suite
- Hashcat 6.2.6+
- MDK4
- Hostapd
- Dnsmasq

## 📦 Installation

### Quick Install
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Computer-Forensic-Toolkit.git
cd Computer-Forensic-Toolkit

# Install Python dependencies
pip install -r requirements.txt --break-system-packages

# Install system tools
sudo apt-get update
sudo apt-get install -y aircrack-ng hashcat mdk4 hostapd dnsmasq
```

### Detailed Installation

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for complete setup instructions.

## 🚀 Usage

### Launch Toolkit
```bash
sudo python3 main.py
```

### Menu Interface
```
=== COMPUTER FORENSIC TOOLKIT ===
[1] Deauthentication Attack
[2] Dictionary Attack (WPA2)
[3] Evil Twin Attack
[4] DoS Authentication Flood
[5] Hashcat Brute-Force
[0] Exit

Select option:
```

### Example: Deauthentication Attack
```bash
sudo python3 main.py
# Select option [1]
# Enter target BSSID: AA:BB:CC:DD:EE:FF
# Enter client MAC: 11:22:33:44:55:66
# Attack executes and evidence saved to /evidence/
```

## 📊 Performance Benchmarks

Tested on Intel Core i7, 16GB RAM, Atheros AR9271:

| Attack Module | Mean Latency | CPU Usage | Memory |
|--------------|-------------|-----------|--------|
| Deauthentication | 24.35s | 2.43% | 14.33 MB |
| Dictionary | 82.29s | 4.39% | 14.42 MB |
| Evil Twin | 253.33s | 2.94% | 14.50 MB |
| DoS Flood | 54.43s | 4.26% | 14.46 MB |
| Hashcat | 62.28s | 3.96% | 14.37 MB |

See dissertation for complete performance analysis (500 experimental iterations).

## ⚖️ Legal Disclaimer

**⚠️ IMPORTANT: Authorized Use Only**

This toolkit is designed exclusively for:
- ✅ Law enforcement forensic investigations with proper legal authorization
- ✅ Controlled laboratory security research
- ✅ Educational purposes in authorized academic environments
- ✅ Penetration testing with explicit written permission from network owners

**Unauthorized use against networks without permission is illegal** and may result in criminal prosecution under:
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Equivalent cybercrime legislation in other jurisdictions

**By using this toolkit, you agree to:**
1. Only use against networks you own or have written authorization to test
2. Comply with all applicable laws and regulations
3. Accept full legal responsibility for your actions
4. Use exclusively for legitimate forensic, research, or educational purposes

The author and Teesside University bear no responsibility for misuse.

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Manual](docs/USAGE.md)
- [Performance Analysis](docs/PERFORMANCE.md)
- [Legal Guidelines](docs/LEGAL.md)
- [Full Dissertation PDF](docs/DISSERTATION.md) *(link to uploaded PDF)*

## 🤝 Contributing

This is an academic project, but suggestions and feedback are welcome:

**Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/Computer-Forensic-Toolkit/issues)

## 📖 Citation

If you use this toolkit in your research, please cite:
```bibtex
@mastersthesis{arshad2026cftoolkit,
  author = {Arshad, Hammad},
  title = {Computer Forensic Toolkit for Police Investigation},
  school = {Teesside University},
  year = {2026},
  type = {MSc Dissertation},
  url = {https://github.com/YOUR_USERNAME/Computer-Forensic-Toolkit}
}
```

## 📧 Contact

**Author:** Hammad Arshad  
**Email:** D3261969@live.tees.ac.uk 
**LinkedIn:** https://www.linkedin.com/in/hammad-arshad-003685141
**University:** Teesside University

## 🙏 Acknowledgments

Special thanks to:
- Mr. Lewis Golightly and Dr. Qiang Guo for supervision and guidance
- Teesside University School of Computing for resources and support
- Open-source security community (Aircrack-ng, Hashcat, MDK4 developers)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

**Developed as part of MSc Cyber Security (with Advanced Practice)**  
**Teesside University | January 2026**
<img width="733" height="1043" alt="Screenshot_2026-01-05_21_38_53" src="https://github.com/user-attachments/assets/76cbea40-bcb6-41ae-86d6-34746707bfb1" />
![Uploading Screenshot_2026-01-05_21_38_53.png…]()

