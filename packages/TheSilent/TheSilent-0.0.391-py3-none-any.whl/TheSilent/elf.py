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
    start = time.time()
    clear()
    hosts = []
    ip_list = []
    
    ip_addr_command = str(run(["ip","addr"], capture_output=True).stdout)
    ip_addr = re.findall("\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}\/\d{2}", ip_addr_command)[0]
    subnet = ipaddress.IPv4Network(ip_addr, strict=False)

    for ip in subnet:
        ip_list.append(str(ip))

    ip_list = random.sample(ip_list[:], len(ip_list[:]))

    print(CYAN + "Checking for hosts!")
    
    for ip in ip_list:
        time.sleep(15)
        my_socket = socket.socket()
        my_socket.settimeout(60)
        print(CYAN + f"checking: {ip}")
        try:
            my_socket.connect((str(ip),80))
            print(CYAN + f"found host: {ip}")
            hosts.append(str(ip))
            my_socket.close()

        except OSError:
            my_socket.close()

        except TimeoutError:
            print(CYAN + f"potential host: {ip}")
            hosts.append(str(ip))
            my_socket.close()

    for ip in ip_list:
        time.sleep(15)
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

    for ip in ip_list:
        time.sleep(15)
        clear()
        print(CYAN + f"Running sqlmap against: http://{ip}")
        os.system(f"sqlmap --url=http://{ip} --random-agent --level=5 --risk=3 --all --forms --flush-session --batch")

    port_list = []
    for port in range(65536):
        port_list.append(port)

    port_list = random.sample(port_list[:], len(port_list[:]))

    for host in ip_list:
        clear()
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
