import sys
from collections import Counter,defaultdict
import re 

IP_PATTERN = re.compile(r"\b(?:(?:\d{1,3}\.){3}\d{1,3}|(?:[A-Fa-f0-9:]+:+)+[A-Fa-f0-9]+)\b")
STATUS_PATTERN = re.compile(r'"\s(\d{3})\s')
VALID_STATUS = {
    "100","101","200","201","204",
    "301","302","304",
    "400","401","403","404",
    "500","502","503"
}

def first_ip_exct(line:str):
    match = IP_PATTERN.search(line)
    return match.group(0) if match else None 

def stat_code_ext(line:str):
    match = STATUS_PATTERN.search(line)
    return match.group(1) if match else None

def main():
    if len(sys.argv) != 2:
        print('Usage python analyzer.py accesslog')
        sys.exit(1)
    
    log_file = sys.argv[1]

    ip_stats = defaultdict(Counter)

    try:
        with open(log_file,'r') as f:
            for line in f:
                ip = first_ip_exct(line)
                stat = stat_code_ext(line)

                if not ip or not stat:
                    continue
                if stat in VALID_STATUS:
                    ip_stats[ip][stat] += 1 
    except FileNotFoundError:
        print(f'File not found: {log_file}')
        sys.exit(1)

    total = Counter({ip:sum(stats.values()) for ip,stats in ip_stats.items()})
    print('===10 IPs with most requests===')
    for ip,count in total.most_common(10):
        print(f'\nIP: {ip:20} | Requests: {count}')
        for status,c in ip_stats[ip].items():
            print(f' {status}: {c}')


if __name__ == '__main__':
    main()