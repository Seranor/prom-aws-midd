import boto3
import time
from datetime import datetime, timedelta
from config.settings import *
from prometheus_client import start_http_server
from mongo_exp.metrics_name import *


def get_cloudwatch_metric_value(metric_name, aws_mongo_type, mongo_instance_id, statistics):
    cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/DocDB',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': aws_mongo_type,
                'Value': mongo_instance_id
            }
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=[statistics]
    )
    # print(response)
    if 'Datapoints' in response:
        datapoints = response['Datapoints']
        if datapoints:
            return datapoints[0][statistics]
    return None


def update_metrics_instance(aws_mongo_type, aws_mongo_instance_id):
    metric_cpu = get_cloudwatch_metric_value('CPUUtilization', aws_mongo_type, aws_mongo_instance_id, 'Average')
    if metric_cpu:
        mongo_cpu_utilization.labels(DocDB=aws_mongo_instance_id).set(metric_cpu)

    metric_mem = get_cloudwatch_metric_value('FreeableMemory', aws_mongo_type, aws_mongo_instance_id, 'Average')
    if metric_mem:
        mongo_freeable_memory.labels(DocDB=aws_mongo_instance_id).set(metric_mem)

    metric_network_throughput = get_cloudwatch_metric_value('NetworkThroughput', aws_mongo_type, aws_mongo_instance_id,
                                                            'Average')
    if metric_network_throughput:
        mongo_network_throughput.labels(DocDB=aws_mongo_instance_id).set(metric_network_throughput)

    metric_read_latency = get_cloudwatch_metric_value('ReadLatency', aws_mongo_type, aws_mongo_instance_id, 'Average')
    if metric_read_latency:
        mongo_read_latency.labels(DocDB=aws_mongo_instance_id).set(metric_read_latency)

    metric_write_latency = get_cloudwatch_metric_value('WriteLatency', aws_mongo_type, aws_mongo_instance_id, 'Average')
    if metric_write_latency:
        mongo_write_latency.labels(DocDB=aws_mongo_instance_id).set(metric_write_latency)


def update_metrics_cluster(aws_mongo_type, aws_mongo_instance_id, ):
    metric_volume_use = get_cloudwatch_metric_value('VolumeBytesUsed', aws_mongo_type, aws_mongo_instance_id, 'Average')
    if metric_volume_use:
        mongo_volume_bytesused.labels(DocDB=aws_mongo_instance_id).set(metric_volume_use)

    metric_volume_readiops = get_cloudwatch_metric_value('VolumeReadIOPs', aws_mongo_type, aws_mongo_instance_id,
                                                         'Average')
    if metric_volume_readiops:
        mongo_volume_readiops.labels(DocDB=aws_mongo_instance_id).set(metric_volume_readiops)

    metric_volume_writeiops = get_cloudwatch_metric_value('VolumeWriteIOPs', aws_mongo_type, aws_mongo_instance_id,
                                                          'Average')
    if metric_volume_writeiops:
        mongo_volume_wriateiops.labels(DocDB=aws_mongo_instance_id).set(metric_volume_writeiops)


def main_loop_aws_mongo_exporter():
    while True:
        for aws_instance_type in AWS_MONGO_INSTANCE_INFO:
            for aws_instance in AWS_MONGO_INSTANCE_INFO.get(aws_instance_type):
                # print(aws_instance_type, aws_instance)
                if aws_instance_type == "DBInstanceIdentifier":
                    update_metrics_instance(aws_instance_type, aws_instance)
                elif aws_instance_type == "DBClusterIdentifier":
                    update_metrics_cluster(aws_instance_type, aws_instance)
                else:
                    print("other or error instance type")
        time.sleep(30)

# if __name__ == '__main__':
#     print(MONGO_AWS_INSTANCE_INFO)
#     start_http_server(9090)
#     while True:
#         for aws_instance_type in MONGO_AWS_INSTANCE_INFO:
#             for aws_instance in MONGO_AWS_INSTANCE_INFO.get(aws_instance_type):
#                 print(aws_instance_type, aws_instance)
#                 if aws_instance_type == "DBInstanceIdentifier":
#                     update_metrics_instance(aws_instance_type, aws_instance)
#                 elif aws_instance_type == "DBClusterIdentifier":
#                     update_metrics_cluster(aws_instance_type, aws_instance)
#         time.sleep(30)
