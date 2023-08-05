# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/materialization/job_metadata.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from tecton_proto.spark_common import clusters_pb2 as tecton__proto_dot_spark__common_dot_clusters__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/tecton_proto/materialization/job_metadata.proto\x12\x1ctecton_proto.materialization\x1a\x1egoogle/protobuf/duration.proto\x1a(tecton_proto/spark_common/clusters.proto\"\x98\x03\n\x0bJobMetadata\x12\x8a\x01\n\"online_store_copier_execution_info\x18\x01 \x01(\x0b\x32<.tecton_proto.materialization.OnlineStoreCopierExecutionInfoH\x00R\x1eonlineStoreCopierExecutionInfo\x12g\n\x14spark_execution_info\x18\x03 \x01(\x0b\x32\x33.tecton_proto.materialization.SparkJobExecutionInfoH\x00R\x12sparkExecutionInfo\x12\x86\x01\n materialization_consumption_info\x18\x02 \x01(\x0b\x32<.tecton_proto.materialization.MaterializationConsumptionInfoR\x1ematerializationConsumptionInfoB\n\n\x08job_info\"?\n\x1eOnlineStoreCopierExecutionInfo\x12\x1d\n\nis_revoked\x18\x01 \x01(\x08R\tisRevoked\"\xdd\x01\n\x15SparkJobExecutionInfo\x12\x15\n\x06run_id\x18\x01 \x01(\tR\x05runId\x12\x1d\n\nis_revoked\x18\x02 \x01(\x08R\tisRevoked\x12\x8d\x01\n#stream_handoff_synchronization_info\x18\x03 \x01(\x0b\x32>.tecton_proto.materialization.StreamHandoffSynchronizationInfoR streamHandoffSynchronizationInfo\"\x91\x02\n StreamHandoffSynchronizationInfo\x12.\n\x13new_cluster_started\x18\x01 \x01(\x08R\x11newClusterStarted\x12;\n\x1astream_query_start_allowed\x18\x02 \x01(\x08R\x17streamQueryStartAllowed\x12@\n\x1cquery_cancellation_requested\x18\x03 \x01(\x08R\x1aqueryCancellationRequested\x12>\n\x1bquery_cancellation_complete\x18\x04 \x01(\x08R\x19queryCancellationComplete\"\xfc\x02\n\x1eMaterializationConsumptionInfo\x12z\n\x19offline_store_consumption\x18\x01 \x01(\x0b\x32>.tecton_proto.materialization.OfflineStoreWriteConsumptionInfoR\x17offlineStoreConsumption\x12w\n\x18online_store_consumption\x18\x02 \x01(\x0b\x32=.tecton_proto.materialization.OnlineStoreWriteConsumptionInfoR\x16onlineStoreConsumption\x12\x65\n\x13\x63ompute_consumption\x18\x03 \x01(\x0b\x32\x34.tecton_proto.materialization.ComputeConsumptionInfoR\x12\x63omputeConsumption\"\xfc\x02\n OfflineStoreWriteConsumptionInfo\x12~\n\x10\x63onsumption_info\x18\x01 \x03(\x0b\x32S.tecton_proto.materialization.OfflineStoreWriteConsumptionInfo.ConsumptionInfoEntryR\x0f\x63onsumptionInfo\x12\\\n\x12offline_store_type\x18\x02 \x01(\x0e\x32..tecton_proto.materialization.OfflineStoreTypeR\x10offlineStoreType\x1az\n\x14\x43onsumptionInfoEntry\x12\x10\n\x03key\x18\x01 \x01(\x03R\x03key\x12L\n\x05value\x18\x02 \x01(\x0b\x32\x36.tecton_proto.materialization.OfflineConsumptionBucketR\x05value:\x02\x38\x01\"h\n\x18OfflineConsumptionBucket\x12!\n\x0crows_written\x18\x01 \x01(\x03R\x0browsWritten\x12)\n\x10\x66\x65\x61tures_written\x18\x02 \x01(\x03R\x0f\x66\x65\x61turesWritten\"\xf6\x02\n\x1fOnlineStoreWriteConsumptionInfo\x12}\n\x10\x63onsumption_info\x18\x01 \x03(\x0b\x32R.tecton_proto.materialization.OnlineStoreWriteConsumptionInfo.ConsumptionInfoEntryR\x0f\x63onsumptionInfo\x12Y\n\x11online_store_type\x18\x02 \x01(\x0e\x32-.tecton_proto.materialization.OnlineStoreTypeR\x0fonlineStoreType\x1ay\n\x14\x43onsumptionInfoEntry\x12\x10\n\x03key\x18\x01 \x01(\x03R\x03key\x12K\n\x05value\x18\x02 \x01(\x0b\x32\x35.tecton_proto.materialization.OnlineConsumptionBucketR\x05value:\x02\x38\x01\"\x8c\x01\n\x17OnlineConsumptionBucket\x12!\n\x0crows_written\x18\x01 \x01(\x03R\x0browsWritten\x12)\n\x10\x66\x65\x61tures_written\x18\x02 \x01(\x03R\x0f\x66\x65\x61turesWritten\x12#\n\rbytes_written\x18\x03 \x01(\x03R\x0c\x62ytesWritten\"\xa0\x01\n\x16\x43omputeConsumptionInfo\x12\x35\n\x08\x64uration\x18\x01 \x01(\x0b\x32\x19.google.protobuf.DurationR\x08\x64uration\x12O\n\rcompute_usage\x18\x02 \x03(\x0b\x32*.tecton_proto.materialization.ComputeUsageR\x0c\x63omputeUsage\"\xbb\x01\n\x0c\x43omputeUsage\x12_\n\x15instance_availability\x18\x01 \x01(\x0e\x32*.tecton_proto.spark_common.AwsAvailabilityR\x14instanceAvailability\x12#\n\rinstance_type\x18\x02 \x01(\tR\x0cinstanceType\x12%\n\x0einstance_count\x18\x03 \x01(\x03R\rinstanceCount*\x8b\x01\n\x0fOnlineStoreType\x12\x1d\n\x19ONLINE_STORE_TYPE_UNKNOWN\x10\x00\x12\x1c\n\x18ONLINE_STORE_TYPE_DYNAMO\x10\x01\x12\x1b\n\x17ONLINE_STORE_TYPE_REDIS\x10\x02\x12\x1e\n\x1aONLINE_STORE_TYPE_BIGTABLE\x10\x03*\x86\x01\n\x10OfflineStoreType\x12\x1e\n\x1aOFFLINE_STORE_TYPE_UNKNOWN\x10\x00\x12\x19\n\x15OFFLINE_STORE_TYPE_S3\x10\x01\x12\x1b\n\x17OFFLINE_STORE_TYPE_DBFS\x10\x02\x12\x1a\n\x16OFFLINE_STORE_TYPE_GCS\x10\x03*\x80\x01\n\x14JobMetadataTableType\x12#\n\x1fJOB_METADATA_TABLE_TYPE_UNKNOWN\x10\x00\x12\"\n\x1eJOB_METADATA_TABLE_TYPE_DYNAMO\x10\x01\x12\x1f\n\x1bJOB_METADATA_TABLE_TYPE_GCS\x10\x02\x42\x1e\n\x1a\x63om.tecton.materializationP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.materialization.job_metadata_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032com.tecton.materializationP\001'
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._options = None
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_options = b'8\001'
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._options = None
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_options = b'8\001'
  _ONLINESTORETYPE._serialized_start=2877
  _ONLINESTORETYPE._serialized_end=3016
  _OFFLINESTORETYPE._serialized_start=3019
  _OFFLINESTORETYPE._serialized_end=3153
  _JOBMETADATATABLETYPE._serialized_start=3156
  _JOBMETADATATABLETYPE._serialized_end=3284
  _JOBMETADATA._serialized_start=156
  _JOBMETADATA._serialized_end=564
  _ONLINESTORECOPIEREXECUTIONINFO._serialized_start=566
  _ONLINESTORECOPIEREXECUTIONINFO._serialized_end=629
  _SPARKJOBEXECUTIONINFO._serialized_start=632
  _SPARKJOBEXECUTIONINFO._serialized_end=853
  _STREAMHANDOFFSYNCHRONIZATIONINFO._serialized_start=856
  _STREAMHANDOFFSYNCHRONIZATIONINFO._serialized_end=1129
  _MATERIALIZATIONCONSUMPTIONINFO._serialized_start=1132
  _MATERIALIZATIONCONSUMPTIONINFO._serialized_end=1512
  _OFFLINESTOREWRITECONSUMPTIONINFO._serialized_start=1515
  _OFFLINESTOREWRITECONSUMPTIONINFO._serialized_end=1895
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_start=1773
  _OFFLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_end=1895
  _OFFLINECONSUMPTIONBUCKET._serialized_start=1897
  _OFFLINECONSUMPTIONBUCKET._serialized_end=2001
  _ONLINESTOREWRITECONSUMPTIONINFO._serialized_start=2004
  _ONLINESTOREWRITECONSUMPTIONINFO._serialized_end=2378
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_start=2257
  _ONLINESTOREWRITECONSUMPTIONINFO_CONSUMPTIONINFOENTRY._serialized_end=2378
  _ONLINECONSUMPTIONBUCKET._serialized_start=2381
  _ONLINECONSUMPTIONBUCKET._serialized_end=2521
  _COMPUTECONSUMPTIONINFO._serialized_start=2524
  _COMPUTECONSUMPTIONINFO._serialized_end=2684
  _COMPUTEUSAGE._serialized_start=2687
  _COMPUTEUSAGE._serialized_end=2874
# @@protoc_insertion_point(module_scope)
