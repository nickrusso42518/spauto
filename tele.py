#!/usr/bin/env python

from cisco_xr_grpc import CiscoXRgRPC
import json

GRPC_ROUTER = "18.206.119.175"


def main():
    """
    1 = test
    2 = gpb
    3 = kvgpb
    4 = json
    """

    with CiscoXRgRPC(host=GRPC_ROUTER) as conn:
        responses = conn.get_subscription("MAC", encode=4)
        for response in responses:
            print(response)


if __name__ == "__main__":
    main()
