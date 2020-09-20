#!/usr/bin/env python

import gnmi_pb2_grpc
import gnmi_pb2
import grpc
import json

#GRPC_ROUTER = "18.206.119.175"
GRPC_ROUTER = "10.10.20.50"  #devbox
GRPC_PORT = 5740

#creds = [("username", "admin"), ("password", "admin")]
creds = [("username", "admin"), ("password", "Cisco123")]

tele_path = "Cisco-IOS-XR-telemetry-model-driven-oper:telemetry-model-driven/destinations/destination"


def main():

    path_str = "Cisco-IOS-XR-infra-rsi-cfg:vrfs"
    #path_str = "openconfig-interfaces"
    get_request = make_get_request(path_str)
    print(get_request)

    with open("../json_config/vrf_c_gnmi.json", "r") as handle:
        vrf_c = json.load(handle)

    update_request = make_set_request(path_str, vrf_c)
    print(update_request)
    replace_request = make_set_request(path_str, vrf_c, operation="replace")
    print(replace_request)
    delete_request = make_set_request(path_str, operation="delete")
    print(delete_request)

    capability_request = make_capability_request()
    print(capability_request)

    subscription_request = make_subscribe_request(tele_path)
    print(subscription_request)

    channel = grpc.insecure_channel(f"{GRPC_ROUTER}:{GRPC_PORT}")
    stub = gnmi_pb2_grpc.gNMIStub(channel)

    #data = stub.Capabilities(capability_request, metadata=creds)
    #print(data)

    #data = stub.Get(get_request, metadata=creds)
    #print(data)

    #data = stub.Set(delete_request, metadata=creds)
    #print(data)

    stream = (n for n in [subscription_request])
    data = stub.Subscribe(stream, metadata=creds)
    for segment in data:
        print(data)


       
def make_path(path_str):
    path_elem = gnmi_pb2.PathElem(name=path_str)
    path = gnmi_pb2.Path(elem=[path_elem])
    return path

def make_get_request(path_str, data_type=1, encoding=4):
    path = make_path(path_str)
    get_request = gnmi_pb2.GetRequest(path=[path], type=0, encoding=encoding)
    return get_request

def make_set_request(path_str, data_dict=None, operation="update"):
    path = make_path(path_str)
    if operation == "delete":
        set_request = gnmi_pb2.SetRequest(delete=[path])
        return set_request

    val_bytes = json.dumps(data_dict).encode("utf-8")
    typed_value = gnmi_pb2.TypedValue(json_ietf_val=val_bytes)
    update = gnmi_pb2.Update(path=path, val=typed_value)

    if operation == "replace":
        set_request = gnmi_pb2.SetRequest(replace=[update])
    elif operation == "update":
        set_request = gnmi_pb2.SetRequest(update=[update])
    else:
        set_request = None

    return set_request

def make_capability_request():
    return gnmi_pb2.CapabilityRequest()

def make_subscribe_request(path_str):
    subscription = gnmi_pb2.Subscription(path=make_path(path_str),
        mode=2, sample_interval=10000000000, suppress_redundant=False)
    subscription_list = gnmi_pb2.SubscriptionList(subscription=[subscription],
        mode=0, encoding=2)
    subscribe_request = gnmi_pb2.SubscribeRequest(subscribe=subscription_list)
    return subscribe_request


if __name__ == "__main__":
    main()
