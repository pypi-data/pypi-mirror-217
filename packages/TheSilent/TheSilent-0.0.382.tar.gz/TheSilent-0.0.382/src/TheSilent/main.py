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
    prCYAN + "")
    clear()

    pr"1 | rogue access point | linux/root")
    pr"2 | arp flooding dos attack | linux/root")
    pr"3 | brute force hash | all")
    pr"4 | dictionary force hash | all")
    pr"5 | hex viewer | all")
    pr"6 | osint | all")
    pr"7 | packet sniffer | linux/root")
    pr"8 | secure overwrite | all/root may be required")
    pr"9 | source code viewer | all")
    pr"10 | web scanner | all")
    pr"")
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
        minimum = input("minimum characters | optional | integer\n")
        maximum = input("maximum characters | optional | integer\n")
        mask = input("mask | optional | string\n")
            
        brute_force_hash(my_hash, minimum, maximum, mask)

    if tool == "4":
        clear()
        my_file = input("file | required | string\n")
        my_hash = input("hash | optional | string\n")
        hash_list = input("file of hashes to crack | optional | string\n")
        mask = input("mask | optional | boolean\n")
        minimum = input("minimum characters | optional | integer\n")
        maximum = input("maximum characters | optional | integer\n")
        dictionary_hash(my_file, my_hash, hash_list, mask, minimum, maximum)

    if tool == "5":
        clear()
        file = input("file | required | string\n")
        hex_viewer(file)

    if tool == "6":
        clear()
        username = input("username | required | string\n")
        delay = input("delay | optional | integer\n")
        tor = input("tor | optional | boolean\n")
        prosusername, delay, tor)

    if tool == "7":
        clear()
        data = input("data | optional | boolean\n")
        hex_dump = input("hex dump | optional | boolean\n")
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
        source_code_viewer(file, keyword)

    if tool == "10":
        clear()
        host = input("host | required | string\n")
        delay = input("delay | optional | integer\n")
        web_scanner(host, delay)

main()
