#!/usr/bin/env python

import grpc
import xr_pb2
import xr_pb2_grpc
import json

GRPC_ROUTER = "18.206.119.175"
GRPC_PORT = 57400


def main():
    creds = [("username", "admin"), ("password", "admin")]
    target = f"{GRPC_ROUTER}:{GRPC_PORT}"
    path = {"Cisco-IOS-XR-ip-static-cfg:router-static": [None]}

    print(f"Connecting to: {target}")
    with grpc.insecure_channel(target) as channel:
        conn = xr_pb2_grpc.gRPCConfigOperStub(channel)

        responses = conn.GetConfig(
            xr_pb2.ConfigGetArgs(yangpathjson=json.dumps(path)), metadata=creds
        )
        for response in responses:
            print(json.loads(response.yangjson))


if __name__ == "__main__":
    main()
