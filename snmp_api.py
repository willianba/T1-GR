from pysnmp.hlapi import *


# noinspection PyBroadException
def run(parameters):
    try:
        error_indication, error_status, error_index, var_binds = next(
            getCmd(SnmpEngine(),
                   CommunityData(parameters['community'], mpModel=0),
                   UdpTransportTarget((parameters['agent'], 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', parameters['object'], parameters['instance']))))

        if error_indication:
            return error_indication
        elif error_status:
            return ('%s at %s' % (error_status.prettyPrint(),
                                  error_index and var_binds[int(error_index) - 1][0] or '?'))
        else:
            for varBind in var_binds:
                return ' = '.join([x.prettyPrint() for x in varBind])
    except Exception:
        return "Something went wrong."
