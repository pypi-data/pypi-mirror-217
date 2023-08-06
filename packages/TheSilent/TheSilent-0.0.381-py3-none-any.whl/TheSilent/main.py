from TheSilent.ap import *
from TheSilent.arp_void import *
from TheSilent.brute_force_hash import *
from TheSilent.clear import *
from TheSilent.dictionary_hash import *
from TheSilent.hex_viewer import *
from TheSilent.osint import *
from TheSilent.packet_sniffer import *
from TheSilent.secure_overwrite import *
from TheSilent.source_code_viewer import *
from TheSilent.web_scanner import *

CYAN = "\033[1;36m"

def main():
    print(CYAN + "")
    clear()

    print("1 | rogue access point | linux/root")
    print("2 | arp flooding dos attack | linux/root")
    print("3 | brute force hash | all")
    print("4 | dictionary force hash | all")
    print("5 | hex viewer | all")
    print("6 | osint | all")
    print("7 | packet sniffer | linux/root")
    print("8 | secure overwrite | all/root may be required")
    print("9 | source code viewer | all")
    print("10 | web scanner | all")
    print("")
    tool = input()

    if tool == "1":
        clear()
        name = input("name | required | string\n")
        interface = input("interface | required | string\n")
        ap(name, interface)

    if tool == "2":
        clear()
        router = input("ip of router | required | string\n")
        interface = input("interface: | required | string\n")
        arp_void(router, interface)

    if tool == "3":
        clear()
        my_hash = input("hash | required | string\n")
        minimum = int(input("minimum characters | optional | integer\n"))
        maximum = int(input("maximum characters | optional | integer\n"))
        mask = input("mask | optional | string\n")
            
        brute_force_hash(my_hash, minimum, maximum, mask)

    if tool == "4":
        clear()
        my_file = input("file | required | string\n")
        my_hash = input("hash | optional | string\n")
        hash_list = input("file of hashes to crack | optional | string\n")
        mask = bool(input("mask | optional | boolean\n"))
        minimum = int(input("minimum characters | optional | integer\n"))
        maximum = int(input("maximum characters | optional | integer\n"))
        dictionary_hash(my_file, my_hash, hash_list, mask, minimum, maximum)

    if tool == "5":
        clear()
        file = input("file | required | string\n")
        hex_viewer(file)

    if tool == "6":
        clear()
        username = input("username | required | string\n")
        delay = int(input("delay | optional | integer\n"))
        tor = bool(input("tor | optional | boolean\n"))
        print(osint(username, delay, tor))

    if tool == "7":
        clear()
        data = bool(input("data | optional | boolean\n"))
        hex_dump = bool(input("hex dump | optional | boolean\n"))
        ip = input("hex dump | optional | string\n")
        protocol = input("protocol | optional | string\n")
        packet_sniffer(data, hex_dump, ip, protocol)

    if tool == "8":
        clear()
        device = input("file, folder, or device | required | string\n")
        secure_overwrite(device)

    if tool == "9":
        clear()
        file = input("file | required | string\n")
        keyword = input("keyword | optional | string\n")
        source_code_viewer(file, keyword="")

    if tool == "10":
        clear()
        host = input("host | required | string\n")
        delay = int(input("delay | optional | integer\n"))
        web_scanner(host, delay)

main()
