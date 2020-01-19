import json
import socket
import subprocess
import sys
from datetime import datetime

# init stuff
start = datetime.now()
with open('config.json') as f:
    config = json.loads(f.read())

"""
Config options:

Host: Host ip or domain

Common Ports: List of common ports to check first
Other (Priority) Ports: List of other ports to check first (after checking common ports).  These ports should not be commonly used ones

Show Closed Ports: (true or false) whether to output closed ports (as closed) or whether to just not output them at all
"""

common_ports = config['common_ports']
other_priority_ports = config['other_ports']
other_ports = list(set(list(range(1, 65535))) - set(common_ports) - set(other_priority_ports))
all_ports = [
    ['Common Ports', common_ports],
    ['Other Priority Ports', other_priority_ports],
    ['All Other Ports', other_ports]
]

host = config['host']
show_closed_ports = config['show_closed_ports']

# Print initializing info
print('Initialized port scanner...')
print(f'Host: "{host}"')
print(f'Common Ports: {common_ports}')
print(f'Other Priority Ports: {other_priority_ports}')
print()

# Scan ports
closed_count = 0
open_count = 0
for category, ports in all_ports:
    print(f'-=[ Scanning {category} ]=-')
    for port in ports:  
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f'Port {port} open')
                open_count += 1
            elif show_closed_ports:
                print(f'Port {port} closed')
                closed_count += 1
            else:
                closed_count += 1
            sock.close()
        except socket.gaierror:
            print('Could not resolve hostname. Terminating program...')
            sys.exit()
        except socket.error as e:
            print(f'Connection failed.  Error: {e}')
            sys.exit()
    
    print() # Formatting

# Print total run time
total_elapsed = datetime.now() - start
print(f'Scanning completed in {total_elapsed.microseconds / 1000}ms')
print(f'Found {open_count} open ports and {closed_count} closed ports')
