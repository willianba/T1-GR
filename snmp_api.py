from easysnmp import snmp_get


# noinspection PyBroadException
def run(parameters):
    try:
        return snmp_get(parameters["object"], hostname=parameters["agent"], community=parameters["community"], version=2).value
    except Exception:
        return "Something went wrong."
