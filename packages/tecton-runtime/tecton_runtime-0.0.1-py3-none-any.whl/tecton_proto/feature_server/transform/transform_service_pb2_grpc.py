# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tecton_proto.feature_server.transform import transform_service_pb2 as tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2


class TransformServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Evaluate = channel.unary_unary(
                '/tecton_proto.feature_server.transform.TransformService/Evaluate',
                request_serializer=tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceRequest.SerializeToString,
                response_deserializer=tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceResponse.FromString,
                )


class TransformServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Evaluate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransformServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Evaluate': grpc.unary_unary_rpc_method_handler(
                    servicer.Evaluate,
                    request_deserializer=tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceRequest.FromString,
                    response_serializer=tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tecton_proto.feature_server.transform.TransformService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TransformService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Evaluate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tecton_proto.feature_server.transform.TransformService/Evaluate',
            tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceRequest.SerializeToString,
            tecton__proto_dot_feature__server_dot_transform_dot_transform__service__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
