#!/bin/bash
set -e

# Adds/removes vlans with bridge to an interaface
# for vlan in {1..10}; do sudo ./vlanadmin.sh $vlan up; done

if [[ $# != 2 ]]; then
    echo "Usage: <vlan-id> <up/down>"
    echo "Example: 1001 up"
    exit
fi
action=$2
vlan=$1

bridge_prefix="brv"
bridge_name="${bridge_prefix}""${vlan}"
interface="bond0"

if [[ $action == "down" ]]; then
    echo "Removing vlan ${vlan} from inteface ${interface}."
    ip link set "${bridge_name}" down
    ip link delete "${bridge_name}" type bridge
    ip link set dev "${interface}"."${vlan}" down
    ip link delete "${interface}"."${vlan}"
elif [[ "${action}" == "up" ]]; then
    echo "Adding vlan ${vlan} to inteface ${interface}."
    ip link add "${bridge_name}" type bridge
    ip link set "${bridge_name}" up
    ip link add link "${interface}" name "${interface}"."${vlan}" type vlan id "${vlan}"
    ip link set dev "${interface}"."${vlan}" up
    ip link set "${interface}"."${vlan}" master "${bridge_name}"
    ip link show "${bridge_name}" 
fi
