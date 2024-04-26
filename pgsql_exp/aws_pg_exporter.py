import boto3
import time
from datetime import datetime, timedelta
from config.settings import *
from pgsql_exp.metrics_name import *

StorageSpace = ""
if AWS_RDS_TYPE == "DBClusterIdentifier":
    StorageSpace = "VolumeBytesUsed"
elif AWS_RDS_TYPE == "DBInstanceIdentifier":
    StorageSpace = "FreeStorageSpace"

CPUUtilization = "CPUUtilization"
FreeableMemory = "FreeableMemory"
NetworkTransmitThroughput = "NetworkTransmitThroughput"
ReadIOPS = "ReadIOPS"


# 建立连接获取指标
def get_cloudwatch_metric_value(metric_name, rds_instance_id, statistics):
    cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/RDS',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': AWS_RDS_TYPE,
                'Value': rds_instance_id
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


def update_metrics():
    #  磁盘使用情况
    disk_space = get_cloudwatch_metric_value(StorageSpace, AWS_RDS_INSTANCE_ID, 'Average')
    if disk_space:
        pg_disk_space.set(disk_space)

    # CPU利用率
    cpu_utilization = get_cloudwatch_metric_value(CPUUtilization, AWS_RDS_INSTANCE_ID, 'Average')
    if cpu_utilization:
        pg_cpu_utilization.set(cpu_utilization)

    # 空闲内存空间
    memory_utilization = get_cloudwatch_metric_value(FreeableMemory, AWS_RDS_INSTANCE_ID, 'Average')
    if memory_utilization:
        pg_memory_utilization.set(memory_utilization)

    # 网络传输吞吐量
    network_throughput = get_cloudwatch_metric_value(NetworkTransmitThroughput, AWS_RDS_INSTANCE_ID, 'Average')
    if network_throughput:
        pg_network_throughput.set(network_throughput)

    # 读取IOPS
    read_iops = get_cloudwatch_metric_value(ReadIOPS, AWS_RDS_INSTANCE_ID, 'Average')
    if read_iops:
        pg_read_iops.set(read_iops)


def main_loop_aws_pg_exporter():
    while True:
        update_metrics()
        time.sleep(30)

# if __name__ == '__main__':
#     # 开始Prometheus HTTP服务器，默认监听在端口8000
#     start_http_server(9090)
#
#     # 定时更新指标
#     while True:
#         update_metrics()
#         time.sleep(10)
