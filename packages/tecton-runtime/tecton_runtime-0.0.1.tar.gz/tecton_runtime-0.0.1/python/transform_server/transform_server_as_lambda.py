from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import ParseDict

from python.transform_server.transform_server import all_transforms
from python.transform_server.transform_server import TransformServerException
from tecton_proto.feature_server.transform import transform_service_pb2


def handler(event, context):
    service_request = ParseDict(event, transform_service_pb2.ServiceRequest())
    try:
        service_response = all_transforms(service_request)
    except TransformServerException as e:
        service_response = transform_service_pb2.ServiceResponse()
        print("Encountered exception: %s", e)
        service_response.error_message = e.details
    return MessageToDict(service_response)
