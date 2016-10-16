#!/usr/bin/env python2
##Simple script to get network equipment interfaces and is easily searchable via datatables https://datatables.net/##
import netsnmp
import validators
import json
import sys
def get_host_interfaces(host, community, version):
    args = {
        "Version": version,
        "DestHost": host,
        "Community": community
    }
    format = 'datatables'
    if not (validators.ip_address.ipv4(host) or validators.ip_address.ipv6(host) or validators.domain(host)):
        return 'invalid hostname/ip'
    out = {}
    data = []
    for idx in netsnmp.snmpwalk(netsnmp.Varbind("IF-MIB::ifIndex"),
                                **args):
        alias, desc, name, ifOperStatus, ifAdminStatus, InOctets, OutOctets = netsnmp.snmpget(
            netsnmp.Varbind("IF-MIB::ifAlias", idx),
            netsnmp.Varbind("IF-MIB::ifDescr", idx),
            netsnmp.Varbind("IF-MIB::ifName", idx),
            #netsnmp.Varbind(".1.3.6.1.2.1.31.1.1.1.1", idx),
            netsnmp.Varbind("IF-MIB::ifOperStatus", idx),
            netsnmp.Varbind("IF-MIB::ifAdminStatus", idx),
            netsnmp.Varbind("IF-MIB::ifInOctets", idx),
            netsnmp.Varbind("IF-MIB::ifOutOctets", idx),
            **args)
        assert(desc is not None and
               InOctets is not None and
               OutOctets is not None)
        if desc == "lo":
            continue
        if ifAdminStatus == '1':
            ifAdminStatus = 'Up'
        elif ifAdminStatus == '2':
            ifAdminStatus = 'Down'
        elif ifAdminStatus == '3':
            ifAdminStatus = 'Testing'
        if ifOperStatus == '1':
            ifOperStatus = 'Up'
        elif ifOperStatus == '2':
            ifOperStatus = 'Down'
        elif ifOperStatus == '3':
            ifOperStatus = 'Testing'
        elif ifOperStatus == '4':
            ifOperStatus = 'Unknown'
        elif ifOperStatus == '5':
            ifOperStatus = 'Dormant'
        elif ifOperStatus == '6':
            ifOperStatus = 'Not Present'
        elif ifOperStatus == '7':
            ifOperStatus = 'Lower Layer Down'
        if format == "pipe":
            print("{}|{}|{}|{}|{}".format(idx, desc, alias, InOctets, OutOctets))
        elif format == "datatables":
            line = []
            line.append(idx)
            line.append(desc)
            line.append(alias)
            line.append(ifOperStatus)
            line.append(ifAdminStatus)
            line.append(InOctets)
            line.append(OutOctets)
        else:
            print("{}|{}|{}|{}|{}".format(idx, desc, alias, ifOperStatus, ifAdminStatus, InOctets, OutOctets))
        data.append(line)
    out = data
    json_out = json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))
    return json_out
if __name__ == "__main__":
    community = 'public'
    version = 2
    if len(sys.argv) < 2:
        print("arg1 must be host/ip address")
        sys.exit()
    host = sys.argv[1]
    if len(sys.argv) == 3:
            community = sys.argv[2]
    if len(sys.argv) == 4:
            version = sys.argv[3]
    a = get_host_interfaces(host, community, version)
    print(a)
