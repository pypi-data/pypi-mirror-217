import ipaddress
import os
import random
import re
import socket
import time
from subprocess import run
from TheSilent.clear import *
from TheSilent.web_scanner import *

CYAN = "\033[1;36m"

def elf():
    port_list = [
        20, # ftp
        21, # ftp
        22, # ssh
        23, # telnet
        25, # smtp
        53, # dns
        67, # dhcp
        68, # dhcp
        69, # tftp
        80, # http
        88, # Kerberos
        110, # pop3
        137, # smb
        138, # smb
        139, # smb
        143, # imap
        443, # https
        445, # smb
        464, # kerberos
        465, # smtp over tls
        853, # secure dns
        636, # ldap over tls
        691, # ms exchange
        902, # vmware server
        989, # ftp over tls
        990, # ftp over tls
        993, # imap over tls
        995, # pop3 over tls
        1194, # openvpn
        1433, # ms sql
        1434, # ms sql
        2483, # oracle db
        2484, # oracle db
        3306, # mysql
        5432, # postgre sql
        8000, # djgano debug
        8001, # django debug
        8080, # alternate http
        8443, # alternate https
        9050, # tor
        9051, # tor
        19132, # minecraft ipv4
        19133 # minecraft ipv6
        ]

    start = time.time()
    clear()
    host_list = []
    ip_list = []
    
    ip_addr_command = str(run(["ip","addr"], capture_output=True).stdout)
    ip_addr = re.findall("\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}\/\d{2}", ip_addr_command)[0]
    subnet = ipaddress.IPv4Network(ip_addr, strict=False)

    for ip in subnet:
        ip_list.append(str(ip))

    ip_list = random.sample(ip_list[:], len(ip_list[:]))

    for ip in ip_list:
        time.sleep(1)
        clear()
        print(CYAN + f"Running The Silent's web scanner against: http://{ip}")
        my_web_scanner = web_scanner(f"http://{ip}")

        with open("report.txt", "a") as file:
            if my_web_scanner == "This server is secure!":
                file.write(f"{ip}: This server is secure!\n")
                print(CYAN + f"{ip}: This server is secure!")

            if my_web_scanner == "This website doesn't exist or is down!":
                file.write(f"{ip}: This website doesn't exist or is down!\n")
                print(CYAN + f"{ip}: This website doesn't exist or is down!")

            else:
                for vuln in my_web_scanner[0]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

                for vuln in my_web_scanner[1]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

        clear()
        print(CYAN + f"Running The Silent's web scanner against: https://{ip}")
        my_web_scanner = web_scanner(f"https://{ip}")

        with open("report.txt", "a") as file:
            if my_web_scanner[0] == "This server is secure!":
                file.write(f"{ip}: This server is secure!\n")
                print(CYAN + f"{ip}: This server is secure!")

            if my_web_scanner == "This website doesn't exist or is down!":
                file.write(f"{ip}: This website doesn't exist or is down!\n")
                print(CYAN + f"{ip}: This website doesn't exist or is down!")

            else:
                for vuln in my_web_scanner[0]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

                for vuln in my_web_scanner[1]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

    ip_list = random.sample(ip_list[:], len(ip_list[:]))
    for ip in ip_list:
        time.sleep(1)
        clear()
        print(CYAN + f"Running sqlmap against: http://{ip}")
        os.system(f"sqlmap --url=http://{ip} --random-agent --level=5 --risk=3 --all --delay=1 --forms --flush-session --batch")

    ip_list = random.sample(ip_list[:], len(ip_list[:]))
    for host in ip_list:
        clear()
        port_list = random.sample(port_list[:], len(port_list[:]))
        print(CYAN + f"Running port scan against: {host}")
        for port in port_list:
            my_socket = socket.socket()
            my_socket.settimeout(60)
            try:
                my_socket.connect((host, port))
                print(f"getting banner: {host}:{port}")
                banner = my_socket.recv(4096)
                print(banner)
                with open("report.txt", "a") as file:
                    file.write(str(banner) + "\n")

                my_socket.close()

            except:
                my_socket.close()
                continue
        
    end = time.time()
    total_time = str(int(end - start))

    clear()
    print("Elf has finished!")
    print(f"Time: {total_time} seconds!")

elf()
