# Web Reconnaissance Tool

A Python-based web reconnaissance tool that automates subdomain enumeration, security header checks, WAF detection, port scanning, and vulnerability detection.

## 🚀 Features
- **Subdomain Enumeration:** Uses `subfinder`, `assetfinder`, and `amass`.
- **Host Probing:** Ensures valid target resolution with `httprobe`.
- **WAF Detection:** Checks for Web Application Firewalls using `wafw00f`.
- **Security Headers Analysis:** Uses `shcheck.py` to detect missing security headers.
- **Port Scanning:** Performs fast service detection with `nmap`.
- **Vulnerability Detection:** Uses `nuclei` for scanning known vulnerabilities.
- **Parallel Execution:** Runs subdomain enumeration tools concurrently.

## 📜 Usage
```bash
python3 intro-web.py -u target.com
```

## 🛠 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Mr-Breeden/web-recon-tool.git
   cd web-recon-tool
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the required tools are installed:
   ```bash
   sudo apt update && sudo apt install nmap amass wafw00f -y

   #Passive online subdomain enumeration
   go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

   #Find domains and subdomains potentially related to a given domain. 
    go install github.com/tomnomnom/assetfinder@latest

   #Take a list of domains and probe for working http and https servers.
   go install github.com/tomnomnom/httprobe@latest

   #Nuclei for vulnerability scanning
   go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

   #SHCheck.py for headers
   git clone https://github.com/s0md3v/SHCheck && cd SHCheck && pip install -r requirements.txt
   ```

## 🔍 How It Works
1. **Ensures HTTPS format** for URL consistency.
2. **Probes host** availability using `httprobe`.
3. **Runs subdomain enumeration** with `subfinder`, `assetfinder`, and `amass` in parallel.
4. **Performs WAF detection** with `wafw00f`.
5. **Checks security headers** using `shcheck.py`.
6. **Scans open ports** using `nmap`.
7. **Identifies vulnerabilities** using `nuclei`.
8. **Saves all results** to separate text files.

## 📄 Output Files
- `subfinder-results-<target>.txt`
- `assetfinder-results-<target>.txt`
- `amass-results-<target>.txt`
- `wafw00f-results-<target>.txt`
- `shcheck-results-<target>.txt`
- `nmap-results-<target>.txt`
- `nuclei-results-<target>.txt`
- `subdomains-results-<target>.txt` (combined subdomain results)

## ⚠️ Disclaimer
This tool is intended for legal security testing and educational purposes only. Ensure you have **permission** before scanning any target.

## 🤝 Contributing
Pull requests and suggestions are welcome!

---

💡 *Stay ethical & happy recon!* 🚀

