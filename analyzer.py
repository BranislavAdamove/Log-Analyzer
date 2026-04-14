import sys
from collections import Counter 


if len(sys.argv) > 2:
    print("Usage: python analyzer.py accesslog")
    sys.exit(1)

log_file = sys.argv[1]
ip_list = Counter()
try:
    with open(log_file,'r') as f:
        for line in f:
            part = f.split()
            if len(part) == 0:
                continue 
            ip = part[1]
            ip_list[ip] += 1 

except FileNotFoundError:
    print(f'File not found: {log_file}')


print("===10 IPS with most Requests===")
for ip,count in ip_list.most_common(10):
    print(f'IP: {ip:20} Number of requests: {count}')