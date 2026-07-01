# Simple TCP Port Scanner

A lightweight multithreaded TCP port scanner written in Python. Warning: Do not try in your country :) 
This project was built as a learning project to practice:

- Python Socket Programming
- Multithreading
- Network Programming
- CLI Development
- Banner Grabbing
- Clean Code Principles

---

## Features

- TCP Port Scanning
- Multithreaded scanning
- Custom port range
- Banner grabbing
- Domain name support
- Colored terminal output
- Scan progress bar
- Scan execution timer
- Common service detection
- Input validation

---

## Installation

Clone the repository:

```bash
git clone https://github.com/iliyahrz/python-port-scanner.git
cd simple-port-scanner
```

Python 3.10+ is recommended.

---

## Usage

Scan the default ports:

```bash
python scanner.py scanme.nmap.org
```

Specify a custom range:

```bash
python scanner.py scanme.nmap.org -s 20 -e 500
```

Specify the number of worker threads:

```bash
python scanner.py scanme.nmap.org -t 200
```

Example:

```bash
python scanner.py 192.168.1.1 -s 1 -e 1024 -t 150
```

---

## Example Output

<img width="893" height="525" alt="Pic1" src="https://github.com/user-attachments/assets/de47fa25-512d-4cb4-92ae-e93372b4a896" />
<img width="752" height="446" alt="Pic2" src="https://github.com/user-attachments/assets/6e3e178a-6085-4367-b9be-3e1b9266603b" />

---

## Project Structure

```
scanner.py
README.md
LICENSE
.gitignore
```

---

## Technologies Used

- Python
- socket
- argparse
- concurrent.futures

---

## Future Improvements

- UDP Scanning
- CIDR Support
- JSON Export
- CSV Export
- Better Banner Detection
- Service Version Detection
- Async Scanning
- as_completed() optimization

---

## Limitations

- TCP only
- IPv4 only
- Banner grabbing depends on the target service
- Does not perform OS detection
- No vulnerability detection

---

## Disclaimer

This tool is intended for educational purposes and authorized security testing only.

The author is not responsible for any misuse.

---

## Author

Developed by **iliyahrz**
