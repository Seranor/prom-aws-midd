from prometheus_client import Gauge, Info

mongo_up = Gauge('mongo_up', 'MongoDB availability')

# mongo 版本
mongo_version = Info('mongo_version', 'MongoDB Version')

# 启动时间
mongo_uptime_seconds = Gauge('mongo_uptime_seconds', 'MongoDB uptime in seconds')

# 当前连接数
mongo_current_connections = Gauge('mongo_current_connections', 'MongoDB current connections')

# 可用的连接数
mongo_available_connections = Gauge('mongo_available_connections', 'MongoDB available connections')

# 总创建的连接数
mongo_totalCreated_connections = Gauge('mongo_totalCreated_connections', 'MongoDB total Created connections')

## 操作计数
# insert
mongo_opcounters_insert = Gauge('mongo_opcounters_insert', 'MongoDB Opcounters Insert')

# query
mongo_opcounters_query = Gauge('mongo_opcounters_query', 'MongoDB Opcounters Query')

# update
mongo_opcounters_update = Gauge('mongo_opcounters_update', 'MongoDB Opcounters Update')

# delete
mongo_opcounters_delete = Gauge('mongo_opcounters_delete', 'MongoDB Opcounters Delete')

# getmore
mongo_opcounters_getmore = Gauge('mongo_opcounters_getmore', 'MongoDB Opcounters Getmore')

# command
mongo_opcounters_command = Gauge('mongo_opcounters_command', 'MongoDB Opcounters Command')
##

## 文档操作统计信息
# deleted
mongo_document_deleted = Gauge('mongo_document_deleted', 'MongoDB Opcounters Deleted')

# inserted
mongo_document_inserted = Gauge('mongo_document_inserted', 'MongoDB Opcounters Inserted')

# returned
mongo_document_returned = Gauge('mongo_document_returned', 'MongoDB Opcounters Returned')

# updated
mongo_document_updated = Gauge('mongo_document_updated', 'MongoDB Opcounters Updated')
##


## 通过 aws cloud watch 获取的值
# CPU 利用率 aws
mongo_cpu_utilization = Gauge('mongo_cpu_utilization', 'MongoDB CPU Utilization', ['DocDB'])

# 可用内存
mongo_freeable_memory = Gauge('mongo_freeable_memory', 'MongoDB FreeableMemory', ['DocDB'])

# 使用存储
mongo_volume_bytesused = Gauge('mongo_volume_bytesused', 'MongoDB VolumeBytesUsed', ['DocDB'])

# 磁盘读 iops
mongo_volume_readiops = Gauge('mongo_volume_readiops', 'MongoDB VolumeReadIOPs', ['DocDB'])

# 磁盘写 iops
mongo_volume_wriateiops = Gauge('mongo_volume_wriateiops', 'MongoDB VolumeWriteIOPs', ['DocDB'])

# 网络吞吐
mongo_network_throughput = Gauge('mongo_network_throughput', 'MongoDB NetworkThroughput', ['DocDB'])

# 读取延迟
mongo_read_latency = Gauge('mongo_read_latency', 'MongoDB ReadLatency', ['DocDB'])

# 写入延迟
mongo_write_latency = Gauge('mongo_write_latency', 'MongoDB WriteLatency', ['DocDB'])


