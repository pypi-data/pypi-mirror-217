# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/data_source_access_config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1tecton_proto/data/data_source_access_config.proto\x12\x11tecton_proto.data\"\x86\x01\n\x1e\x44\x61taSourceAccessConfigurations\x12\x64\n\x18workspace_configurations\x18\x01 \x03(\x0b\x32).tecton_proto.data.WorkspaceConfigurationR\x17workspaceConfigurations\"{\n\x16WorkspaceConfiguration\x12%\n\x0eworkspace_name\x18\x01 \x01(\tR\rworkspaceName\x12:\n\x19\x61llowed_instance_profiles\x18\x02 \x03(\tR\x17\x61llowedInstanceProfilesB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.data_source_access_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _DATASOURCEACCESSCONFIGURATIONS._serialized_start=73
  _DATASOURCEACCESSCONFIGURATIONS._serialized_end=207
  _WORKSPACECONFIGURATION._serialized_start=209
  _WORKSPACECONFIGURATION._serialized_end=332
# @@protoc_insertion_point(module_scope)
