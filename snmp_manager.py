import time
import dao
import snmp_api
from helpers import *
from settings import *
from snmp_settings import SNMPSettings
from tkinter import ttk, Frame, Label, Entry, Button, LabelFrame, StringVar, Text, LEFT, END, INSERT
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from threading import Thread


# noinspection PyBroadException
class SNMPManager:
    def __init__(self, master=None):
        # setup tab objects
        self.master = master
        self.navigation_tabs = ttk.Notebook(self.master)
        self.setup = Frame(self.navigation_tabs)
        self.setup.pack()
        self.title_container = Frame(self.setup)
        self.title = Label(self.title_container, text="SNMP Manager")
        self.create_title()
        self.agent_container = Frame(self.setup)
        self.agent_label = Label(self.agent_container, text="Agent IP:", font=font, width=label_width)
        self.agent = Entry(self.agent_container)
        self.create_agent()
        self.community_container = Frame(self.setup)
        self.community_label = Label(self.community_container, text="Community:", font=font,
                                     width=label_width)
        self.community = Entry(self.community_container)
        self.create_community()
        self.object_container = Frame(self.setup)
        self.object_label = Label(self.object_container, text="Object instance:", font=font, width=label_width)
        self.object = Entry(self.object_container)
        self.create_object()
        self.time_container = Frame(self.setup)
        self.time_label = Label(self.time_container, text="Refresh time (s):", font=font, width=label_width)
        validation = self.time_container.register(only_numbers)
        self.time = Entry(self.time_container, validate="key", validatecommand=(validation, '%S'))
        self.create_charts = False
        self.create_time()
        self.buttons_container = Frame(self.setup)
        self.get_object = Button(self.buttons_container, text="Get Object", font=font, width=button_width)
        self.settings = Button(self.buttons_container, text="Settings", font=font, width=button_width)
        self.start_monitor = Button(self.buttons_container, text="Start monitor", font=font, width=button_width)
        self.stop_monitor = Button(self.buttons_container, text="Stop monitor", font=font, width=button_width)
        self.create_setup_buttons()
        # results frames
        self.result_tabs = ttk.Notebook(self.setup)
        self.response_label_frame = LabelFrame(self.result_tabs, font=font)
        self.response_value = StringVar(self.response_label_frame)
        self.response_text = Text(self.response_label_frame, font=font)
        self.warning_label_frame = LabelFrame(self.result_tabs, font=font)
        self.warning_value = StringVar(self.warning_label_frame)
        self.warning_text = Text(self.warning_label_frame, font=font)
        self.create_result()
        # charts objects
        self.link_chart = Frame(self.navigation_tabs)
        self.ip_chart = Frame(self.navigation_tabs)
        self.tcp_chart = Frame(self.navigation_tabs)
        self.udp_chart = Frame(self.navigation_tabs)
        self.icmp_chart = Frame(self.navigation_tabs)
        self.snmp_chart = Frame(self.navigation_tabs)
        self.create_charts_frames()
        self.assemble_tabs()
        # placeholders
        self.threads = None
        self.link = 0
        self.link_list = []
        self.ip_send = 0
        self.ip_receive = 0
        self.ip_send_list = []
        self.ip_receive_list = []
        self.tcp_send = 0
        self.tcp_receive = 0
        self.tcp_send_list = []
        self.tcp_receive_list = []
        self.udp_send = 0
        self.udp_receive = 0
        self.udp_send_list = []
        self.udp_receive_list = []
        self.icmp_send = 0
        self.icmp_receive = 0
        self.icmp_send_list = []
        self.icmp_receive_list = []
        self.snmp_send = 0
        self.snmp_receive = 0
        self.snmp_send_list = []
        self.snmp_receive_list = []

    def create_title(self):
        self.title_container["pady"] = 10
        self.title["font"] = title_font
        self.title_container.pack()
        self.title.pack()

    def create_agent(self):
        set_container_padding(self.agent_container)
        set_entry_configuration(self.agent)
        self.agent_container.pack()
        self.agent_label.pack(side=LEFT)
        self.agent.pack(side=LEFT)

    def create_community(self):
        set_container_padding(self.community_container)
        set_entry_configuration(self.community)
        self.community_container.pack()
        self.community_label.pack(side=LEFT)
        self.community.pack(side=LEFT)

    def create_object(self):
        set_container_padding(self.object_container)
        set_entry_configuration(self.object)
        self.object_container.pack()
        self.object_label.pack(side=LEFT)
        self.object.pack(side=LEFT)

    def create_time(self):
        set_container_padding(self.time_container)
        set_entry_configuration(self.time)
        self.time_container.pack()
        self.time_label.pack(side=LEFT)
        self.time.pack(side=LEFT)

    def create_setup_buttons(self):
        set_container_padding(self.buttons_container)
        self.get_object["command"] = lambda: self.get_snmp_object()
        self.start_monitor["command"] = lambda: self.start_charts_monitor()
        self.stop_monitor["command"] = lambda: self.stop_charts_monitor()
        self.settings["command"] = lambda: self.set_settings()
        self.buttons_container.pack()
        self.get_object.pack(side=LEFT)
        self.start_monitor.pack(side=LEFT)
        self.stop_monitor.pack(side=LEFT)
        self.settings.pack(side=LEFT)

    def create_result(self):
        self.response_value.set("")
        self.warning_value.set("")
        self.response_label_frame.pack()
        self.warning_label_frame.pack()
        self.result_tabs.add(self.response_label_frame, text="Response")
        self.result_tabs.add(self.warning_label_frame, text="Warning")
        self.response_text.pack()
        self.warning_text.pack()
        self.result_tabs.pack()

    def create_charts_frames(self):
        self.link_chart.pack()
        self.ip_chart.pack()
        self.tcp_chart.pack()
        self.udp_chart.pack()
        self.icmp_chart.pack()
        self.snmp_chart.pack()

    def assemble_tabs(self):
        self.navigation_tabs.add(self.setup, text="Setup")
        self.navigation_tabs.add(self.link_chart, text="Link")
        self.navigation_tabs.add(self.ip_chart, text="IP")
        self.navigation_tabs.add(self.tcp_chart, text="TCP")
        self.navigation_tabs.add(self.udp_chart, text="UDP")
        self.navigation_tabs.add(self.icmp_chart, text="ICMP")
        self.navigation_tabs.add(self.snmp_chart, text="SNMP")
        self.navigation_tabs.pack()

    def get_snmp_object(self):
        try:
            parameters = self.extract_snmp_parameters()
            snmp_response = snmp_api.run(parameters)
            self.response_value.set(snmp_response)
        except IndexError:
            self.response_value.set("Object must contain an instance.")
        self.update_return_value()

    def extract_snmp_parameters(self):
        snmp_object = self.object.get().split(".")
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": snmp_object[0],
            "instance": snmp_object[1]
        }
        return parameters

    def clear_return_value(self):
        self.response_text.delete("1.0", END)

    def update_return_value(self):
        self.clear_return_value()
        self.response_text.insert(INSERT, self.response_value.get())

    def start_charts_monitor(self):
        self.create_charts = True
        self.create_threads()
        for thread in self.threads:
            thread.daemon = True
            thread.start()

    def create_threads(self):
        self.threads = [
            Thread(target=self.create_link_chart),
            Thread(target=self.create_ip_chart),
            Thread(target=self.create_tcp_chart),
            Thread(target=self.create_udp_chart),
            Thread(target=self.create_icmp_chart),
            Thread(target=self.create_snmp_chart)
        ]

    def create_link_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.link = self.get_link_utilization() - self.link
            self.link_list.append(self.link)
            self.verify_link_limits()
            while self.create_charts:
                self.clear_link_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.plot(self.link_list)
                ax.set_title("Link utilization")
                graph = FigureCanvasTkAgg(fig, master=self.link_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating link chart.\n")
            self.update_warning_value()

    def verify_link_limits(self):
        limits = dao.get_limits_from_link()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.link < inferior or self.link > superior:
            self.warning_value.set("Link is out of defined limits.\n")
            self.update_warning_value()

    def get_link_utilization(self):
        input_octets = self.get_input_octets()
        output_octets = self.get_output_octets()
        if_speed = self.get_if_speed()
        return (input_octets + output_octets) * 8 / if_speed

    def get_input_octets(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifInOctets",
            "instance": "0"
        }
        return int(snmp_api.run(parameters))

    def get_output_octets(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifOutOctets",
            "instance": "0"
        }
        return int(snmp_api.run(parameters))

    def get_if_speed(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifSpeed",
            "instance": "0"
        }
        return int(snmp_api.run(parameters))

    def create_ip_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.ip_send = self.get_ip_send_percentage() - self.ip_send
            self.ip_receive = self.get_ip_receive_percentage() - self.ip_receive
            self.ip_send_list.append(self.ip_send)
            self.ip_receive_list.append(self.ip_receive)
            self.verify_ip_limits()
            while self.create_charts:
                self.clear_ip_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.set_ylabel("% of packets")
                ax.set_title("IP send/receive")
                ax.plot(self.ip_send_list, label="Send")
                ax.plot(self.ip_receive_list, label="Receive")
                ax.legend(loc=0)
                graph = FigureCanvasTkAgg(fig, master=self.ip_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating IP chart.\n")
            self.update_warning_value()

    def verify_ip_limits(self):
        limits = dao.get_limits_from_ip()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.ip_send < inferior or self.ip_send > superior or self.ip_receive < inferior or self.ip_receive > superior:
            self.warning_value.set("IP is out of defined limits.\n")
            self.update_warning_value()

    def get_ip_send_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ipInDelivers",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_sent_packets()

    def get_ip_receive_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ipOutRequests",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_received_packets()

    def create_tcp_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.tcp_send = self.get_tcp_send_percentage()
            self.tcp_receive = self.get_tcp_receive_percentage()
            self.tcp_send_list.append(self.tcp_send)
            self.tcp_receive_list.append(self.tcp_receive)
            self.verify_tcp_limits()
            while self.create_charts:
                self.clear_tcp_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.set_ylabel("% of packets")
                ax.set_title("TCP send/receive")
                ax.plot(self.tcp_send_list, label="Send")
                ax.plot(self.tcp_receive_list, label="Receive")
                ax.legend(loc=0)
                graph = FigureCanvasTkAgg(fig, master=self.tcp_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating TCP chart.\n")
            self.update_warning_value()

    def verify_tcp_limits(self):
        limits = dao.get_limits_from_tcp()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.tcp_send < inferior or self.tcp_send> superior or self.tcp_receive < inferior or self.tcp_receive > superior:
            self.warning_value.set("TCP is out of defined limits.\n")
            self.update_warning_value()

    def get_tcp_send_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "tcpOutSegs",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_sent_packets()

    def get_tcp_receive_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "tcpInSegs",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_received_packets()

    def create_udp_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.udp_send = self.get_udp_send_percentage() - self.udp_send
            self.udp_receive = self.get_udp_receive_percentage() - self.udp_receive
            self.udp_send_list.append(self.udp_send)
            self.udp_receive_list.append(self.udp_receive)
            self.verify_udp_limits()
            while self.create_charts:
                self.clear_udp_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.set_ylabel("% of packets")
                ax.set_title("UDP send/receive")
                ax.plot(self.udp_send_list, label="Send")
                ax.plot(self.udp_receive_list, label="Receive")
                ax.legend(loc=0)
                graph = FigureCanvasTkAgg(fig, master=self.udp_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating UDP chart.\n")
            self.update_warning_value()

    def verify_udp_limits(self):
        limits = dao.get_limits_from_udp()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.udp_send < inferior or self.udp_send> superior or self.udp_receive < inferior or self.udp_receive > superior:
            self.warning_value.set("UDP is out of defined limits.\n")
            self.update_warning_value()

    def get_udp_send_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "udpOutDatagrams",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_sent_packets()

    def get_udp_receive_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "udpInDatagrams",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_received_packets()

    def create_icmp_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.icmp_send = self.get_icmp_send_percentage() - self.icmp_send
            self.icmp_receive = self.get_icmp_receive_percentage() - self.icmp_receive
            self.icmp_send_list.append(self.icmp_send)
            self.icmp_receive_list.append(self.icmp_receive)
            self.verify_icmp_limits()
            while self.create_charts:
                self.clear_icmp_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.set_ylabel("% of packets")
                ax.set_title("ICMP send/receive")
                ax.plot(self.icmp_send_list, label="Send")
                ax.plot(self.icmp_receive_list, label="Receive")
                ax.legend(loc=0)
                graph = FigureCanvasTkAgg(fig, master=self.icmp_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating ICMP chart.\n")
            self.update_warning_value()

    def verify_icmp_limits(self):
        limits = dao.get_limits_from_icmp()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.icmp_send < inferior or self.icmp_send> superior or self.icmp_receive < inferior or self.icmp_receive > superior:
            self.warning_value.set("ICMP is out of defined limits.\n")
            self.update_warning_value()

    def get_icmp_send_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "icmpOutMsgs",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_sent_packets()

    def get_icmp_receive_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "icmpInMsgs",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_received_packets()

    def create_snmp_chart(self):
        try:
            refresh_time = self.get_refresh_time()
            self.snmp_send = self.get_snmp_send_percentage() - self.snmp_send
            self.snmp_receive = self.get_snmp_receive_percentage() - self.snmp_receive
            self.snmp_send_list.append(self.snmp_send)
            self.snmp_receive_list.append(self.snmp_receive)
            self.verify_snmp_limits()
            while self.create_charts:
                self.clear_snmp_chart()
                fig = Figure()
                ax = fig.add_subplot()
                ax.grid()
                ax.set_ylabel("% of packets")
                ax.set_title("SNMP send/receive")
                ax.plot(self.snmp_send_list, label="Send")
                ax.plot(self.snmp_receive_list, label="Receive")
                ax.legend(loc=0)
                graph = FigureCanvasTkAgg(fig, master=self.snmp_chart)
                graph.get_tk_widget().pack()
                time.sleep(refresh_time)
        except Exception:
            self.warning_value.set("Error creating SNMP chart.\n")
            self.update_warning_value()

    def verify_snmp_limits(self):
        limits = dao.get_limits_from_snmp()[0]
        inferior = limits[0]
        superior = limits[1]
        if self.snmp_send < inferior or self.snmp_send> superior or self.snmp_receive < inferior or self.snmp_receive > superior:
            self.warning_value.set("SNMP is out of defined limits.\n")
            self.update_warning_value()

    def get_snmp_send_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "snmpOutPkts",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_sent_packets()

    def get_snmp_receive_percentage(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "snmpInPkts",
            "instance": "0"
        }
        return int(snmp_api.run(parameters)) * 100 / self.get_received_packets()

    def get_sent_packets(self):
        u_parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifOutUcastPkts",
            "instance": "0"
        }
        nu_parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifOutNUcastPkts",
            "instance": "0"
        }
        u_packets = int(snmp_api.run(u_parameters))
        nu_packets = int(snmp_api.run(nu_parameters))
        return u_packets + nu_packets

    def get_received_packets(self):
        u_parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifInUcastPkts",
            "instance": "0"
        }
        nu_parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": "ifInNUcastPkts",
            "instance": "0"
        }
        u_packets = int(snmp_api.run(u_parameters))
        nu_packets = int(snmp_api.run(nu_parameters))
        return u_packets + nu_packets

    def clear_link_chart(self):
        for child in self.link_chart.winfo_children():
            child.destroy()

    def clear_ip_chart(self):
        for child in self.ip_chart.winfo_children():
            child.destroy()

    def clear_tcp_chart(self):
        for child in self.tcp_chart.winfo_children():
            child.destroy()

    def clear_udp_chart(self):
        for child in self.udp_chart.winfo_children():
            child.destroy()

    def clear_icmp_chart(self):
        for child in self.icmp_chart.winfo_children():
            child.destroy()

    def clear_snmp_chart(self):
        for child in self.snmp_chart.winfo_children():
            child.destroy()

    def get_refresh_time(self):
        try:
            refresh_time = int(self.time.get())
            if refresh_time > 0:
                self.clear_warning_value()
                return refresh_time
        except Exception:
            self.warning_value.set("Refresh time must be higher than zero.\n")
            self.update_warning_value()
            return 0

    def clear_warning_value(self):
        self.warning_text.delete("1.0", END)

    def update_warning_value(self):
        self.warning_text.insert(INSERT, self.warning_value.get())

    def stop_charts_monitor(self):
        self.create_charts = False

    def set_settings(self):
        SNMPSettings(self.master)
