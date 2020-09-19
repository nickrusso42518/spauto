#!/usr/bin/env python

import grpc
import xr_pb2
import xr_pb2_grpc
import json


class CiscoXRgRPC:
    def __init__(self, host, port=57400, username="admin", password="admin"):
        self.creds = [("username", username), ("password", password)]
        self.channel = None
        self.conn = None
        self.host = host
        self.port = port

    def __enter__(self):
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = xr_pb2_grpc.gRPCConfigOperStub(self.channel)
        return self

    def __exit__(self, type, value, traceback):
        self.channel.close()

    def get_config(self, yangpathjson_dict):
        responses = self.stub.GetConfig(
            xr_pb2.ConfigGetArgs(yangpathjson=json.dumps(yangpathjson_dict)),
            metadata=self.creds,
        )
        return [json.loads(resp.yangjson) for resp in responses]

    def _make_config_args(self, data):
        return xr_pb2.ConfigArgs(yangjson=json.dumps(data))

    def merge_config(self, yangjson_dict):
        response = self.stub.MergeConfig(
            self._make_config_args(yangjson_dict), metadata=self.creds
        )
        return response

    def delete_config(self, yangjson_dict):
        response = self.stub.DeleteConfig(
            self._make_config_args(yangjson_dict), metadata=self.creds
        )
        return response

    def replace_config(self, yangjson_dict):
        response = self.stub.ReplaceConfig(
            self._make_config_args(yangjson_dict), metadata=self.creds
        )
        return response

    # everything under this comment is untested
    def commit_config(self, label, comment):
        commit_msg = xr_pb2.CommitMsg(label=label, comment=comment)
        response = self.stub.CommitConfig(
            xr_pb2.CommitArgs(CommitMsg=commit_msg, metadata=self.creds)
        )
        return response


    def get_subscription(self, sub_id, encode=3):
        """Telemetry subscription function
            :param sub_id: Subscription ID
            :type: string
            :return: Returns discrete values emitted by telemetry stream
            :rtype: JSON formatted string
        """
        sub_args = xr_pb2.CreateSubsArgs(ReqId=1, encode=encode, subidstr=sub_id)
        stream = self.stub.CreateSubs(sub_args, metadata=self.creds)
        for segment in stream:
            yield segment
