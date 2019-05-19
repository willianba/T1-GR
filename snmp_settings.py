from settings import *
from helpers import *
from tkinter import Frame, Label, Entry, LEFT, Toplevel, Button
import dao


def get_settings_from_db():
    link = dao.get_limits_from_link()
    ip = dao.get_limits_from_ip()
    tcp = dao.get_limits_from_tcp()
    udp = dao.get_limits_from_udp()
    icmp = dao.get_limits_from_icmp()
    snmp = dao.get_limits_from_snmp()
    return {
        "link": {
            "inferior": link[0][0],
            "superior": link[0][1]
        },
        "ip": {
            "inferior": ip[0][0],
            "superior": ip[0][1]
        },
        "tcp": {
            "inferior": tcp[0][0],
            "superior": tcp[0][1]
        },
        "udp": {
            "inferior": udp[0][0],
            "superior": udp[0][1]
        },
        "icmp": {
            "inferior": icmp[0][0],
            "superior": icmp[0][1]
        },
        "snmp": {
            "inferior": snmp[0][0],
            "superior": snmp[0][1]
        }
    }


def save_settings_into_db(settings):
    dao.update_limits_for_link(settings["link"])
    dao.update_limits_for_ip(settings["ip"])
    dao.update_limits_for_tcp(settings["tcp"])
    dao.update_limits_for_udp(settings["udp"])
    dao.update_limits_for_icmp(settings["icmp"])
    dao.update_limits_for_snmp(settings["snmp"])


class SNMPSettings:
    def __init__(self, master=None):
        # settings screen
        root = Toplevel(master)
        self.settings = get_settings_from_db()
        self.screen = Frame(root)
        self.screen.pack()
        self.title_container = Frame(self.screen)
        self.title = Label(self.title_container, text="SNMP Settings")
        self.create_title()
        # link limits
        self.link_container = Frame(self.screen)
        self.link_label = Label(self.link_container, text="Link limits", width=label_width)
        self.link_superior_label = Label(self.link_container, text="Superior limit:", font=font, width=label_width)
        self.link_inferior_label = Label(self.link_container, text="Inferior limit:", font=font, width=label_width)
        self.link_superior_limit = Entry(self.link_container)
        self.link_inferior_limit = Entry(self.link_container)
        self.create_link()
        # ip limits
        self.ip_container = Frame(self.screen)
        self.ip_label = Label(self.ip_container, text="IP limits", width=label_width)
        self.ip_superior_label = Label(self.ip_container, text="Superior limit:", font=font, width=label_width)
        self.ip_inferior_label = Label(self.ip_container, text="Inferior limit:", font=font, width=label_width)
        self.ip_superior_limit = Entry(self.ip_container)
        self.ip_inferior_limit = Entry(self.ip_container)
        self.create_ip()
        # tcp limits
        self.tcp_container = Frame(self.screen)
        self.tcp_label = Label(self.tcp_container, text="TCP limits", width=label_width)
        self.tcp_superior_label = Label(self.tcp_container, text="Superior limit:", font=font, width=label_width)
        self.tcp_inferior_label = Label(self.tcp_container, text="Inferior limit:", font=font, width=label_width)
        self.tcp_superior_limit = Entry(self.tcp_container)
        self.tcp_inferior_limit = Entry(self.tcp_container)
        self.create_tcp()
        # udp limits
        self.udp_container = Frame(self.screen)
        self.udp_label = Label(self.udp_container, text="UDP limits", width=label_width)
        self.udp_superior_label = Label(self.udp_container, text="Superior limit:", font=font, width=label_width)
        self.udp_inferior_label = Label(self.udp_container, text="Inferior limit:", font=font, width=label_width)
        self.udp_superior_limit = Entry(self.udp_container)
        self.udp_inferior_limit = Entry(self.udp_container)
        self.create_udp()
        # icmp limits
        self.icmp_container = Frame(self.screen)
        self.icmp_label = Label(self.icmp_container, text="ICMP limits", width=label_width)
        self.icmp_superior_label = Label(self.icmp_container, text="Superior limit:", font=font, width=label_width)
        self.icmp_inferior_label = Label(self.icmp_container, text="Inferior limit:", font=font, width=label_width)
        self.icmp_superior_limit = Entry(self.icmp_container)
        self.icmp_inferior_limit = Entry(self.icmp_container)
        self.create_icmp()
        # snmp limits
        self.snmp_container = Frame(self.screen)
        self.snmp_label = Label(self.snmp_container, text="SNMP limits", width=label_width)
        self.snmp_superior_label = Label(self.snmp_container, text="Superior limit:", font=font, width=label_width)
        self.snmp_inferior_label = Label(self.snmp_container, text="Inferior limit:", font=font, width=label_width)
        self.snmp_superior_limit = Entry(self.snmp_container)
        self.snmp_inferior_limit = Entry(self.snmp_container)
        self.create_snmp()
        # save button
        self.save_container = Frame(self.screen)
        self.save_button = Button(self.save_container, text="Save settings", font=font, width=button_width)
        self.create_button()

    def create_title(self):
        self.title_container["pady"] = 10
        self.title["font"] = title_font
        self.title_container.pack()
        self.title.pack()

    def create_link(self):
        set_container_padding(self.link_container)
        set_entry_configuration(self.link_inferior_limit)
        self.link_label["font"] = title_font
        self.link_inferior_limit.insert(0, self.settings["link"]["inferior"])
        self.link_superior_limit.insert(0, self.settings["link"]["superior"])
        self.link_container.pack()
        self.link_label.pack()
        self.link_inferior_label.pack(side=LEFT)
        self.link_inferior_limit.pack(side=LEFT)
        self.link_superior_label.pack(side=LEFT)
        self.link_superior_limit.pack(side=LEFT)

    def create_ip(self):
        set_container_padding(self.ip_container)
        set_entry_configuration(self.ip_inferior_limit)
        self.ip_label["font"] = title_font
        self.ip_inferior_limit.insert(0, self.settings["ip"]["inferior"])
        self.ip_superior_limit.insert(0, self.settings["ip"]["superior"])
        self.ip_container.pack()
        self.ip_label.pack()
        self.ip_inferior_label.pack(side=LEFT)
        self.ip_inferior_limit.pack(side=LEFT)
        self.ip_superior_label.pack(side=LEFT)
        self.ip_superior_limit.pack(side=LEFT)

    def create_tcp(self):
        set_container_padding(self.tcp_container)
        set_entry_configuration(self.tcp_inferior_limit)
        self.tcp_label["font"] = title_font
        self.tcp_inferior_limit.insert(0, self.settings["tcp"]["inferior"])
        self.tcp_superior_limit.insert(0, self.settings["tcp"]["superior"])
        self.tcp_container.pack()
        self.tcp_label.pack()
        self.tcp_inferior_label.pack(side=LEFT)
        self.tcp_inferior_limit.pack(side=LEFT)
        self.tcp_superior_label.pack(side=LEFT)
        self.tcp_superior_limit.pack(side=LEFT)

    def create_udp(self):
        set_container_padding(self.udp_container)
        set_entry_configuration(self.udp_inferior_limit)
        self.udp_label["font"] = title_font
        self.udp_inferior_limit.insert(0, self.settings["udp"]["inferior"])
        self.udp_superior_limit.insert(0, self.settings["udp"]["superior"])
        self.udp_container.pack()
        self.udp_label.pack()
        self.udp_inferior_label.pack(side=LEFT)
        self.udp_inferior_limit.pack(side=LEFT)
        self.udp_superior_label.pack(side=LEFT)
        self.udp_superior_limit.pack(side=LEFT)

    def create_icmp(self):
        set_container_padding(self.icmp_container)
        set_entry_configuration(self.icmp_inferior_limit)
        self.icmp_label["font"] = title_font
        self.icmp_inferior_limit.insert(0, self.settings["icmp"]["inferior"])
        self.icmp_superior_limit.insert(0, self.settings["icmp"]["superior"])
        self.icmp_container.pack()
        self.icmp_label.pack()
        self.icmp_inferior_label.pack(side=LEFT)
        self.icmp_inferior_limit.pack(side=LEFT)
        self.icmp_superior_label.pack(side=LEFT)
        self.icmp_superior_limit.pack(side=LEFT)

    def create_snmp(self):
        set_container_padding(self.snmp_container)
        set_entry_configuration(self.snmp_inferior_limit)
        self.snmp_label["font"] = title_font
        self.snmp_inferior_limit.insert(0, self.settings["snmp"]["inferior"])
        self.snmp_superior_limit.insert(0, self.settings["snmp"]["superior"])
        self.snmp_container.pack()
        self.snmp_label.pack()
        self.snmp_inferior_label.pack(side=LEFT)
        self.snmp_inferior_limit.pack(side=LEFT)
        self.snmp_superior_label.pack(side=LEFT)
        self.snmp_superior_limit.pack(side=LEFT)

    def create_button(self):
        set_container_padding(self.save_container)
        self.save_button["command"] = lambda: self.save()
        self.save_container.pack()
        self.save_button.pack()

    def save(self):
        self.settings["link"]["inferior"] = int(self.link_inferior_limit.get())
        self.settings["link"]["superior"] = int(self.link_superior_limit.get())
        self.settings["ip"]["inferior"] = int(self.ip_inferior_limit.get())
        self.settings["ip"]["superior"] = int(self.ip_superior_limit.get())
        self.settings["tcp"]["inferior"] = int(self.tcp_inferior_limit.get())
        self.settings["tcp"]["superior"] = int(self.tcp_superior_limit.get())
        self.settings["udp"]["inferior"] = int(self.udp_inferior_limit.get())
        self.settings["udp"]["superior"] = int(self.udp_superior_limit.get())
        self.settings["icmp"]["inferior"] = int(self.icmp_inferior_limit.get())
        self.settings["icmp"]["superior"] = int(self.icmp_superior_limit.get())
        self.settings["snmp"]["inferior"] = int(self.snmp_inferior_limit.get())
        self.settings["snmp"]["superior"] = int(self.snmp_superior_limit.get())
        save_settings_into_db(self.settings)
