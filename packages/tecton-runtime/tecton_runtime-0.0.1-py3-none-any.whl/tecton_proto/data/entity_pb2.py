# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/entity.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.validation import validator_pb2 as tecton__proto_dot_validation_dot_validator__pb2
from tecton_proto.data import fco_metadata_pb2 as tecton__proto_dot_data_dot_fco__metadata__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etecton_proto/data/entity.proto\x12\x11tecton_proto.data\x1a\'tecton_proto/validation/validator.proto\x1a$tecton_proto/data/fco_metadata.proto\x1a\x1ctecton_proto/common/id.proto\"\x94\x02\n\x06\x45ntity\x12\x34\n\tentity_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x08\x65ntityId\x12\x1b\n\tjoin_keys\x18\x03 \x03(\tR\x08joinKeys\x12\x41\n\x0c\x66\x63o_metadata\x18\x07 \x01(\x0b\x32\x1e.tecton_proto.data.FcoMetadataR\x0b\x66\x63oMetadata\x12V\n\x0fvalidation_args\x18\t \x01(\x0b\x32-.tecton_proto.validation.EntityValidationArgsR\x0evalidationArgsJ\x04\x08\x02\x10\x03J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07J\x04\x08\x08\x10\tB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.entity_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _ENTITY._serialized_start=163
  _ENTITY._serialized_end=439
# @@protoc_insertion_point(module_scope)
