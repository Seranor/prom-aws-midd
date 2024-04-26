from prometheus_client import Gauge

# 创建 Prometheus 指标
# 数据库对应的大小
pg_database_size_bytes = Gauge('pg_database_size_bytes', 'Size of databases in bytes', ['database_name'])

# 用户对应的连接数
pg_user_connection_count = Gauge('pg_user_connection_count', 'Number of connections per user', ['username'])

# 数据库总连接数
pg_total_connections = Gauge('pg_total_connections', 'Total number of connections')

# 数据库活跃的连接数
pg_active_connections = Gauge('pg_active_connections', 'Number of active connections')

# 数据库空闲连接数
pg_idle_connections = Gauge('pg_idle_connections', 'Number of idle connections')

# 数据库启动时间 秒
pg_uptime_seconds = Gauge('pg_uptime_seconds', 'PostgreSQL uptime in seconds')

# 数据库是否能连接
pg_up = Gauge('pg_up', 'PostgreSQL database availability')

# 数据库所有的qps
pg_qps_all = Gauge('pg_qps_all', 'PostgreSQL Queries per second ALL')

# 数据库 读 qps
pg_qps_read = Gauge('pg_qps_read', 'PostgreSQL Queries per second read')

# 数据库 写 qps
pg_qps_write = Gauge('pg_qps_write', 'PostgreSQL Queries per second write')

# 每秒处于等待的会话数有多少
pg_wait_session_sec = Gauge('pg_wait_session_sec', 'PostgreSQL Number of waiting sessions per second')

# 每5秒处于等待的会话数有多少
pg_wait_session_five_sec = Gauge('pg_wait_session_five_sec', 'PostgreSQL Number of waiting sessions per five second')

## 通过 aws cloud watch 获取的值
# 剩余存储空间 或者 存储使用量
pg_disk_space = Gauge('pg_storage_disk_space', 'PostgreSQL Disk Space')

# CPU 利用率 aws
pg_cpu_utilization = Gauge('pg_cpu_utilization', 'PostgreSQL CPU Utilization')

# 空闲内存空间
pg_memory_utilization = Gauge('pg_memory_utilization', 'PostgreSQL Memory Utilization')

# 网络传输吞吐量
pg_network_throughput = Gauge('pg_network_throughput', 'PostgreSQL network throughput')

# 读取IOPS
pg_read_iops = Gauge('pg_read_iops', 'PostgreSQL read IOPS')
##

pg_query_calls = Gauge('pg_query_calls', 'Number of calls', ['query'])
pg_query_total_exec_time = Gauge('pg_query_total_exec_time', 'Execution time', ['query'])
pg_query_min_exec_time = Gauge('pg_query_min_exec_time', 'Min Exec Time', ['query'])
pg_query_max_exec_time = Gauge('pg_query_max_exec_time', 'Max Exec Time', ['query'])
pg_query_mean_exec_time = Gauge('pg_query_mean_exec_time', 'Mean Exec Time', ['query'])
pg_query_blk_read_time = Gauge('pg_query_blk_read_time', 'Block read time', ['query'])
pg_query_blk_write_time = Gauge('pg_query_blk_write_time', 'Block write time', ['query'])
pg_query_rows = Gauge('pg_query_rows', 'Number of rows', ['query'])
pg_query_hit_percent = Gauge('pg_query_hit_percent', 'Cache hit percentage', ['query'])
