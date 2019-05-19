from tkinter import Tk
from snmp_manager import SNMPManager

root = Tk()
root.geometry("500x400")
root.title("SNMP Manager")
SNMPManager(root)
root.mainloop()
exit()
