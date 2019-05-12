from tkinter import *
from pysnmp.hlapi import *


def only_numbers(char):
    return char.isdigit()


class Application:
    def __init__(self, master=None):
        self.label_width = 15
        self.font = ("Verdana", "8")
        self.input = Frame(master)
        self.create_input_section()
        self.title_container = Frame(self.input)
        self.title = Label(self.title_container, text="SNMP Manager")
        self.create_title()
        self.agent_container = Frame(self.input)
        self.agent_label = Label(self.agent_container, text="Agent IP:", font=self.font, width=self.label_width)
        self.agent = Entry(self.agent_container)
        self.create_agent()
        self.community_container = Frame(self.input)
        self.community_label = Label(self.community_container, text="Community:", font=self.font,
                                     width=self.label_width)
        self.community = Entry(self.community_container)
        self.create_community()
        self.object_container = Frame(self.input)
        self.object_label = Label(self.object_container, text="Object instance:", font=self.font,
                                  width=self.label_width)
        self.object = Entry(self.object_container)
        self.create_object()
        self.time_container = Frame(self.input)
        self.time_label = Label(self.time_container, text="Refresh time (s):", font=self.font, width=self.label_width)
        validation = self.time_container.register(only_numbers)
        self.time = Entry(self.time_container, validate="key", validatecommand=(validation, '%S'))
        self.create_time()
        self.run_container = Frame(self.input)
        self.run_button = Button(self.run_container, text="Run", font=self.font, width=self.label_width)
        self.create_run_button()
        self.return_container = Frame(self.input)
        self.return_label_frame = LabelFrame(self.return_container, text="Response", font=self.font)
        self.return_value = StringVar(self.return_label_frame)
        self.return_text = Text(self.return_label_frame, font=self.font)
        self.create_return()

    def create_input_section(self):
        self.input.pack()

    def create_title(self):
        self.title_container["pady"] = 10
        self.title_container.pack()
        self.title["font"] = ("Calibri", "9", "bold")
        self.title.pack()

    def create_agent(self):
        self.agent_container["padx"] = 20
        self.agent_container["pady"] = 5
        self.agent_container.pack()
        self.agent_label.pack(side=LEFT)
        self.agent["width"] = 25
        self.agent["font"] = self.font
        self.agent.pack(side=LEFT)

    def create_community(self):
        self.community_container["padx"] = 20
        self.community_container["pady"] = 5
        self.community_container.pack()
        self.community_label.pack(side=LEFT)
        self.community["width"] = 25
        self.community["font"] = self.font
        self.community.pack(side=LEFT)

    def create_object(self):
        self.object_container["padx"] = 20
        self.object_container["pady"] = 5
        self.object_container.pack()
        self.object_label.pack(side=LEFT)
        self.object["width"] = 25
        self.object["font"] = self.font
        self.object.pack(side=LEFT)

    def create_time(self):
        self.time_container["padx"] = 20
        self.time_container["pady"] = 5
        self.time_container.pack()
        self.time_label.pack(side=LEFT)
        self.time["width"] = 25
        self.time["font"] = self.font
        self.time.pack(side=LEFT)

    def create_run_button(self):
        self.run_container.pack()
        self.run_button["command"] = lambda: self.execute_actions()
        self.run_button.pack(side=LEFT)

    def create_return(self):
        self.return_container.pack()
        self.return_label_frame.pack()
        self.return_value.set("")
        self.return_text.pack()

    def extract_parameters(self):
        parameters = {
            "agent": self.agent.get(),
            "community": self.community.get(),
            "object": self.object.get().split(".")[0],
            "instance": self.object.get().split(".")[1],
            "time": self.time.get()
        }
        return parameters

    def execute_actions(self):
        try:
            parameters = self.extract_parameters()
            self.run_snmp(parameters)
        except IndexError:
            self.return_value.set("Object must contain an instance.")
        self.update_return_value()

    def update_return_value(self):
        self.return_text.delete("1.0", END)
        self.return_text.insert(INSERT, self.return_value.get())

    def run_snmp(self, parameters):
        try:
            error_indication, error_status, error_index, var_binds = next(
                getCmd(SnmpEngine(),
                       CommunityData(parameters['community'], mpModel=0),
                       UdpTransportTarget((parameters['agent'], 161)),
                       ContextData(),
                       ObjectType(ObjectIdentity('SNMPv2-MIB', parameters['object'], parameters['instance']))))

            if error_indication:
                self.return_value.set(error_indication)
            elif error_status:
                self.return_value.set('%s at %s' % (error_status.prettyPrint(),
                                      error_index and var_binds[int(error_index) - 1][0] or '?'))
            else:
                for varBind in var_binds:
                    self.return_value.set(' = '.join([x.prettyPrint() for x in varBind]))
        except Exception:
            self.return_value.set("Something went wrong.")


root = Tk()
root.geometry("400x250")
Application(root)
root.mainloop()
