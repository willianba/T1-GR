import netsnmp
import argparse
import sys


def run_snmp(args):
  var = netsnmp.Varbind(args.object) 
  netsnmp.snmpget(var, Version=args.version, DestHost=args.agent, Community=args.community)
  print('{0}.{1}: {2}'.format(var.tag, var.iid, var.val))


def main():
  ap = argparse.ArgumentParser(description="SNMP Manager", prog="app")
  ap.add_argument("-a", "--agent", required=True, help="Agent IP or Hostname")
  ap.add_argument("-o", "--object", required=True, help="SNMP object")
  ap.add_argument("-c", "--community", default="public", help="SNMP community [default = public]")
  ap.add_argument("-v", "--version", default=2, help="SNMP version (1 or 2) [default = 2]")
  args = ap.parse_args()
  run_snmp(args)

if __name__ == "__main__":
  main()
