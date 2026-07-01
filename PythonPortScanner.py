from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    gethostbyname,
    gaierror
)
import argparse
from time import perf_counter
from sys import exit
from concurrent.futures import ThreadPoolExecutor

SERVICES = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP Alternate"
}
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "BLUE": "\033[94m",
    "YELLOW": "\033[93m",
    "RESET": "\033[0m"
}


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple TCP Port Scanner")
    parser.add_argument("target", help="Target IP or Domain")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start Port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End Port")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of worker threads")
    args = parser.parse_args()

    valid = validation(args)
    if valid:
        parser.error(valid)
    return args


def validation(args):
    if not (1 <= args.start <= 65535):
        return "Start port must be between 1 and 65535."
    elif not (1 <= args.end <= 65535):
        return "End port must be between 1 and 65535."
    elif args.start > args.end:
        return "Start port cannot be greater than end port."
    elif not (1 <= args.threads <= 500):
        return "Threads must be between 1 and 500."
    return None


def resolve_target(target):
    try:
        return gethostbyname(target)
    except gaierror:
        return None


def scan_port(port, target_ip):
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                banner = grab_banner(sock)
                service = SERVICES.get(port, "Unknown")
                return {"port": port,
                            "service": service,
                                "banner": banner or "N/A"}

    except OSError:
        pass


def grab_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024)
        return banner.decode(errors="ignore").strip()

    except Exception:
        return None


def run_scan(target, start, end, threads):
    results = []

    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for port in range(start, end + 1):
                futures.append(executor.submit(scan_port, port, target))
            done = 0
            for future in futures:
                result = future.result()
                if result: results.append(result)
                done += 1
                print(f"\r{show_progress(done, end-start+1)} Scanning {done}/{end-start+1}", end="")

        return results

    except KeyboardInterrupt:
        return 2
    except Exception:
        return 0


def show_progress(done, total):
    progress = done / total
    bar_length = 35
    filled = int(progress * bar_length)
    bar = ("█" * filled + "-" * (bar_length - filled))
    percent = progress * 100
    return f"[{bar}] {percent:.1f}%"


def main():
    args = parse_arguments()
    target_ip = resolve_target(args.target)

    if not target_ip:
        print("Cannot resolve target.")
        exit(1)

    print(F"Starting scan for {args.target}({target_ip}) from {args.start} to {args.end}")

    start_time = perf_counter()
    results = run_scan(target_ip, args.start, args.end, args.threads)
    end_time = perf_counter()
    match results:
        case 2:
            print(COLORS["RED"] + "\nScan canceled by user." + COLORS['RESET'])
            return 2
        case 0:
            print(COLORS["RED"] + "UNKNOWN ERROR!" + COLORS['RESET'])
            return 0
        case _:
            print(f"{COLORS["BLUE"]}\nFinished in {end_time - start_time:.2f} seconds.{COLORS["RESET"]}")
            for i in results:
                print(f"{COLORS["GREEN"]}[OPEN]",
                      i["port"],
                      f"{COLORS["YELLOW"]}{i["service"]}{COLORS['RESET']}",
                      f"{COLORS["BLUE"]}{i["banner"]}{COLORS['RESET']}",
                      "=" * 30,
                      sep="\n")
            print("ALL OPEN PORTS IN ONE LINE 👍")
            for result in results:
                print(f"{COLORS["GREEN"]}{result["port"]}{COLORS["RESET"]}", end=" - ")
            print(COLORS["BLUE"] + "IS OPEN" + COLORS["RESET"])
            return True


if __name__ == "__main__":
    main()