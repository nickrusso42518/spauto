#!/usr/bin/env python

from cisco_xr_grpc import CiscoXRgRPC
import json

GRPC_ROUTER = "18.206.119.175"


def main():

    # Dict that gets converted to a string (per protobuf) to identify the
    # YANG data to collect
    paths = {
        "static": {"Cisco-IOS-XR-ip-static-cfg:router-static": [None]},
        "vrf": {"Cisco-IOS-XR-infra-rsi-cfg:vrfs": [None]},
        "bgp": {"Cisco-IOS-XR-ipv4-bgp-cfg:bgp": [None]},
    }

    with CiscoXRgRPC(host=GRPC_ROUTER) as conn:
        for name, path in paths.items():
            print(f"\nCollecting {name} config:")
            responses = conn.get_config(yangpathjson_dict=path)
            for response in responses:
                print(json.dumps(response, indent=2))


if __name__ == "__main__":
    main()
