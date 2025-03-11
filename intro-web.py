import subprocess
import sys
import os
import concurrent.futures
import nmap

# Colors class for colored output
class Colors:
    RESET = "\33[0m"
    BOLD = "\33[1m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    CYAN = "\33[36m"

def break_and_help():
    """Quit and show help message."""
    print("\n\t   [?] Usage example: intro-web -u target.com")
    exit()

def ensure_https(url):
    """Ensure URL starts with https:// if not already specified."""
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url

def run_command(command, output_file):
    """Run a shell command and write output to a file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.DEVNULL, check=True)
        print(f"[*] Finished: {command}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error while running command: {command}\n{e}")

def run_subdomain_tools_concurrently(URL_TARGET):
    """Run subfinder, assetfinder, and amass concurrently."""
    print("[*] Running subdomain enumeration tools concurrently...")

    commands = {
        "subfinder": f"subfinder -d {URL_TARGET} -silent",
        "assetfinder": f"assetfinder {URL_TARGET}",
        "amass": f"amass enum -d {URL_TARGET} -silent"
    }

    output_files = {
        "subfinder": f"subfinder-results-{URL_TARGET}.txt",
        "assetfinder": f"assetfinder-results-{URL_TARGET}.txt",
        "amass": f"amass-results-{URL_TARGET}.txt"
    }

    # Run tools concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_command, cmd, output_files[tool]): tool for tool, cmd in commands.items()}

        for future in concurrent.futures.as_completed(futures):
            tool = futures[future]
            try:
                future.result()
                print(f"[+] {tool.capitalize()} completed successfully.")
            except Exception as e:
                print(f"[!] {tool.capitalize()} failed: {e}")

    # Combine results
    combined_file = f"subdomains-results-{URL_TARGET}.txt"
    try:
        with open(combined_file, "w", encoding="utf-8") as combined:
            for tool, file_path in output_files.items():
                with open(file_path, "r", encoding="utf-8") as tool_file:
                    combined.writelines(tool_file.readlines())
        print(f"[*] Combined subdomain results saved to {combined_file}")
    except FileNotFoundError as e:
        print(f"[!] Error combining subdomain results: {e}")

# Main script logic
if __name__ == "__main__":
    port_scan = nmap.PortScanner()

    command_arguments = sys.argv[1:]

    if len(command_arguments) > 0:
        flag = command_arguments[0].upper()

        if flag == "-U" or flag == "--URL":
            URL_TARGET = command_arguments[1]
        else:
            break_and_help()
    else:
        break_and_help()

    # Ensure the correct format for tools that require HTTPS
    URL_TARGET_HTTPS = ensure_https(URL_TARGET)

    # Recon phase
    print(Colors.BOLD + Colors.CYAN + f"\n\t[*] Starting recon on {URL_TARGET}:" + Colors.RESET)

    # Run httprobe to check host
    try:
        print("[*] Running: httprobe to check host")
        httprobe_command = f"echo {URL_TARGET} | httprobe -prefer-https"
        get_host = subprocess.check_output(httprobe_command, shell=True, text=True).strip()
        print(f"[*] Host resolved to: {get_host}")
    except subprocess.TimeoutExpired:
        print("[!] Command 'httprobe' timed out after 15 seconds.")
        exit()

    # Check for WAF using wafw00f
    def check_waf(url):
        try:
            print("[*] Running: wafw00f to check for WAF...")

            waf_file = f"wafw00f-results-{URL_TARGET}.txt"

            # Ensure file is created before attempting to write to it
            with open(waf_file, "w", encoding="utf-8") as f:
                f.write("")

            waf_result = subprocess.check_output(f"wafw00f {url}", shell=True, text=True)

            with open(waf_file, "w", encoding="utf-8") as f:
                f.write(waf_result)

            if "not detected" in waf_result:
                print("[+] No WAF detected.")
            else:
                print("[!] WAF Detected:\n" + waf_result.strip())

        except subprocess.CalledProcessError as e:
            print(f"[!] Error while running wafw00f: {e}")
        except OSError as e:
            print(f"[!] File operation error: {e}")

    check_waf(URL_TARGET_HTTPS)

    # Check Security Headers using shcheck.py
    try:
        print("[*] Running: shcheck.py to check for security headers...")
        shcheck_file = f"shcheck-results-{URL_TARGET}.txt"
        shcheck_result = subprocess.check_output(f"shcheck.py -d {URL_TARGET_HTTPS}", shell=True, text=True)
        with open(shcheck_file, "w", encoding="utf-8") as f:
            f.write(shcheck_result)
        if "not detected" in shcheck_result:
            print("[+] Header issue detected.")
        else:
            print("[!] Security headers:\n" + shcheck_result.strip())
    except subprocess.CalledProcessError as e:
        print(f"[!] Error while running shcheck.py: {e}")

    # Run Nmap to scan ports
    try:
        print("[*] Scanning ports using Nmap...")
        nmap_file = f"nmap-results-{URL_TARGET}.txt"
        nmap_command = f"nmap {URL_TARGET} -oN {nmap_file} -F -sV"
        subprocess.run(nmap_command, shell=True, check=True)
        print(f"[*] Nmap results saved to {nmap_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error while running Nmap: {e}")

    # Run subdomain enumeration tools concurrently
    run_subdomain_tools_concurrently(URL_TARGET)

    # Run nuclei for vulnerability detection
    try:
        print("[*] Running: nuclei for vulnerability detection...")
        nuclei_file = f"nuclei-results-{URL_TARGET}.txt"
        nuclei_command = f"nuclei -u {URL_TARGET_HTTPS} -silent -o {nuclei_file}"
        subprocess.run(nuclei_command, shell=True, check=True)
        print(f"[*] Nuclei results saved to {nuclei_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error while running nuclei: {e}")

    print(Colors.BOLD + Colors.GREEN + "[*] Recon completed successfully!" + Colors.RESET)
