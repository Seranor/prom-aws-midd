import boto3
import time
from datetime import datetime, timedelta
from redis_exp.metrics_name import *
from config.settings import *
from prometheus_client import start_http_server


def get_cloudwatch_metric_value(metric_name, aws_cache_type, cache_instance_id, statistics):
    cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/ElastiCache',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': aws_cache_type,
                'Value': cache_instance_id
            }
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=[statistics]
    )
    if 'Datapoints' in response:
        datapoints = response['Datapoints']
        if datapoints:
            return datapoints[0][statistics]
    return None


def update_metrics(cache_type, cache_instance):
    metrics1 = get_cloudwatch_metric_value('NetworkBandwidthInAllowanceExceeded', cache_type, cache_instance,
                                           'Average')
    if metrics1 is not None:
        redis_network_bandwidth_inallowance_exceeded.labels(ElastiCache=cache_instance).set(metrics1)

    metrics2 = get_cloudwatch_metric_value('NetworkBandwidthInAllowanceExceeded', cache_type, cache_instance,
                                           'Average')
    if metrics2 is not None:
        redis_network_bandwidthOut_allowance_exceeded.labels(ElastiCache=cache_instance).set(metrics2)

    metrics3 = get_cloudwatch_metric_value('NetworkConntrackAllowanceExceeded', cache_type, cache_instance,
                                           'Average')
    if metrics3 is not None:
        redis_network_conntrack_allowance_exceeded.labels(ElastiCache=cache_instance).set(metrics3)

    metrics4 = get_cloudwatch_metric_value('NetworkPacketsPerSecondAllowanceExceeded', cache_type, cache_instance,
                                           'Average')
    if metrics4 is not None:
        redis_network_packetsPerSecond_allowance_exceeded.labels(ElastiCache=cache_instance).set(metrics4)


def main_loop_aws_redis_exporter():
    while True:
        for cache_type in AWS_ELASTICACHE_INSTANCE_INFO:
            for cache_instance in AWS_ELASTICACHE_INSTANCE_INFO.get(cache_type):
                # print(cache_type, cache_instance)
                update_metrics(cache_type, cache_instance)
        time.sleep(60)


if __name__ == '__main__':
    start_http_server(9090)
    main_loop_aws_redis_exporter()
