#!/usr/bin/env python

from cisco_xr_grpc import CiscoXRgRPC
import json

GRPC_ROUTER = "18.206.119.175"


def main():

    # Dict that gets converted to a string (per protobuf) to identify the
    # YANG data to collect
    paths = {
        #"static": {"Cisco-IOS-XR-ip-static-cfg:router-static": [None]},
        #"vrf": {"Cisco-IOS-XR-infra-rsi-cfg:vrfs": {"vrf": [{"vrf-name": "A"}]}},
        #"bgp": {"Cisco-IOS-XR-ipv4-bgp-cfg:bgp": [None]},
        "vrf": {"Cisco-IOS-XR-infra-rsi-cfg:vrfs": [None]},
    }
    vrf_b = {"Cisco-IOS-XR-infra-rsi-cfg:vrfs": {"vrf": [{"vrf-name": "B"}]}},

    with open("json_config/vrf_c.json", "r") as handle:
        vrf_c = json.load(handle)

    with CiscoXRgRPC(host=GRPC_ROUTER) as conn:
        """
        for name, path in paths.items():
            print(f"\nCollecting {name} config:")
            responses = conn.get_config(yangpathjson_dict=path)
            for response in responses:
                print(json.dumps(response, indent=2))
        """

        # merge vrf C
        #response = conn.merge_config(yangjson_dict=vrf_c)

        # delete vrf B
        #response = conn.delete_config(yangjson_dict=vrf_b)

        # replace vrf C
        response = conn.replace_config(yangjson_dict=vrf_c)


if __name__ == "__main__":
    main()
