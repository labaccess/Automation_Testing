from pysnmp.hlapi import (
    SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity, nextCmd # <--- Add nextCmd here
)

def snmp_walk(host, community='public', port=161, oid='1.3.6.1.2.1'):
    """
    Performs an SNMP walk on the specified host and OID.

    Args:
        host (str): The IP address or hostname of the SNMP agent.
        community (str): The SNMP community string (default: 'public').
        port (int): The UDP port for SNMP (default: 161).
        oid (str): The starting OID for the walk (default: '1.3.6.1.2.1' for MIB-2).
    """
    print(f"Performing SNMP walk on {host}:{port} with community '{community}' starting from OID: {oid}")
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(community),
                              UdpTransportTarget((host, port)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lookupMib=True,
                              lexicographicalMode=True):

        if errorIndication:
            print(f"Error: {errorIndication}")
            break
        elif errorStatus:
            print(f"Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

if __name__ == "__main__":
    # Replace '192.168.1.1' with the actual IP address of your device
    # and 'public' with your SNMP community string if it's different.
    snmp_walk('192.168.1.1', community='public')