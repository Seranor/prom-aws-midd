## AWS Middleware Monitoring Replenish
### 说明
```bash
1.通过 AWS 的 cloudwatch 获取到 pgsql 相应的指标
2.python连接pgsql执行SQL得到监控所需的值 拼装为我们所需要的指标
```

**注意PGSQL需要开启pg_stat_statements 扩展, SQL命令: CREATE EXTENSION pg_stat_statements;**
### 环境变量信息
| 变量名称                          | 值                     |
|-------------------------------|-----------------------|
| PG_DATABASE                   | PG的IP或者URL            |
| PG_PORT                       | PG的端口                 |
| PG_USER                       | 用户名                   |
| PG_PWD                        | 密码                    |
| PG_DBNAME                     | 数据库名称                 |
| AWS_REGION                    | AWS地区                 |
| AWS_ACCESS_KEY_ID             | aws 的秘钥ID             |
| AWS_SECRET_ACCESS_KEY         | aws的秘钥                |
| AWS_RDS_INSTANCE_ID           | pgsql实例名称             |
| SERVER_PORT                   | 不写该变量 端口默认 9010       |
| AWS_RDS_TYPE                  | PGSQL_RDS 的类型         |
| MONGO_INFO                    | MongoDB连接信息           |
| AWS_MONGO_INSTANCE_INFO       | aws的MongoDB实例类型和id    |
| AWS_ELASTICACHE_INSTANCE_INFO | aws中elasticcache类型和id |

AWS_RDS_TYPE的值为
```bash
DBClusterIdentifier
对应的引擎为 Aurora PostgreSQL
pg_storage_disk_space 此时无值, AWS 性质决定

DBInstanceIdentifier
对应的引擎为 PostgreSQL
pg_storage_disk_space 此时为剩余磁盘存储量
```
MONGO_INFO
```bash
AWS中 DocDB的 连接方式 比较特别
{"connect": {"address": "HOST","port": "PORT","user": "xxx","pwd": "xxx"},"parameter": {"authSource": "admin","tls": "true","tlsCAFile": "global-bundle.pem","replicaSet": "rs0","readPreference": "secondaryPreferred","retryWrites": "false"}}
```

AWS_MONGO_INSTANCE_INFO
```bash
依据AWS的实例情况来
{"DBInstanceIdentifier": ["dev-staging", "dev-staging2"],"DBClusterIdentifier": ["dev-staging"]}
```

AWS_ELASTICACHE_INSTANCE_INFO
```bash
依据 ElasticCache 情况
{"CacheClusterId": ["staging-001"]}
```

### 指标名称及含义
| 指标名称                                              | 含义                   |
|---------------------------------------------------|----------------------|
| pg_database_size_bytes                            | 每个数据库对应的大小           |
| pg_user_connection_count                          | 用户对应的连接数             |
| pg_total_connections                              | 数据库总连接数              |
| pg_active_connections                             | 数据库活跃的连接数            |
| pg_idle_connections                               | 数据库空闲连接数             |
| pg_uptime_seconds                                 | 数据库启动时间 单位秒          |
| pg_up                                             | 数据库是否能连接             |
| pg_qps_all                                        | 数据库所有的qps            |
| pg_qps_read                                       | 数据库 读 qps            |
| pg_qps_write                                      | 数据库 写 qps            |
| pg_wait_session_sec                               | 每秒处于等待的会话数有多少        |
| pg_wait_session_five_sec                          | 每5秒处于等待的会话数有多少       |
| pg_storage_disk_space                             | 剩余存储空间               |
| pg_cpu_utilization                                | CPU 利用率              |
| pg_memory_utilization                             | 空闲内存空间               |
| pg_network_throughput                             | 网络传输吞吐量              |
| pg_read_iops                                      | 读取IOPS               |
| pg_query_calls                                    | 执行次数                 |
| pg_query_total_exec_time                          | 执行语句所花费的总时间（以毫秒为单位）  |
| pg_query_min_exec_time                            | 执行语句所花费的最短时间（以毫秒为单位） |
| pg_query_max_exec_time                            | 执行语句所花费的最长时间         |
| pg_query_mean_exec_time                           | 执行语句所花费的平均时间（以毫秒为单位） |
| pg_query_blk_read_time                            | 句读取块所花费的总时间，以毫秒为单位   |
| pg_query_blk_write_time                           | 语句写入块所花费的总时间，以毫秒为单位  |
| pg_query_rows                                     | 语句检索或影响的总行数          |
| pg_query_hit_percent                              | 缓存命中率                |
| mongo_up                                          | mongo是否能正常或者连接问题     |
| mongo_version                                     | mongo版本              |
| mongo_uptime_seconds                              | 启动时间 单位秒             |
| mongo_current_connections                         | 当前连接数                |
| mongo_available_connections                       | 可用的连接数               |
| mongo_totalCreated_connections                    | 总创建的连接数              |
| mongo_opcounters_insert                           | 操作计数insert           |
| mongo_opcounters_query                            | 操作计数query            |
| mongo_opcounters_update                           | 操作计数update           |
| mongo_opcounters_delete                           | 操作计数delete           |
| mongo_opcounters_getmore                          | 操作计数getmore          |
| mongo_opcounters_command                          | 操作计数command          |
| mongo_document_deleted                            | 文档操作统计deleted        |
| mongo_document_inserted                           | 文档操作统计inserted       |
| mongo_document_returned                           | 文档操作统计returned       |
| mongo_document_updated                            | 文档操作统计updated        |
| mongo_cpu_utilization                             | CPU 当前使用率            |
| mongo_freeable_memory                             | 剩余可用内存 字节            |
| mongo_volume_bytesused                            | 使用存储 字节              |
| mongo_volume_readiops                             | 磁盘读 iops             |
| mongo_volume_wriateiops                           | 磁盘写 iops             |
| mongo_network_throughput                          | 网络吞吐                 |
| mongo_read_latency                                | 读取延迟                 |
| mongo_write_latency                               | 写入延迟                 |
| redis_network_bandwidth_inallowance_exceeded      | 超出了入站网络带宽限额          |
| redis_network_bandwidthOut_allowance_exceeded     | 超出了出站网络带宽限额          |
| redis_network_conntrack_allowance_exceeded        | 超出了网络连接跟踪限额          |
| redis_network_packetsPerSecond_allowance_exceeded | 超出了每秒网络数据包限额         |




### 运行服务
Docker 构建镜像
```bash
docker build -t [registry]:[version] -f Dockerfile .

默认端口 9010

运行时需要添加上述的环境变量信息
```
Kubernetes
```bash

```
### Grafana模板

在grafana目录中
PG的Dashboard需要结合 postgres_exporter 一起
https://github.com/prometheus-community/postgres_exporter
### TODO


### kafka说明 disable
```bash
 KAFKA_SERVER       KAFKA server
 PG_ENV_NAME        pgsql 实例环境(相当于tag) 
 
该功能是将 pgsql 的 SQL 执行时间做统计录入到 KAFKA --> Logstash --> ES --> Kibana

该服务的 topic 名称叫 pgsql_query_message

logstash 消费 pgsql_query_message 
关于 query_sql 是通过 ELK 录入到 elasticsearch中


logstash 创建索引
    input { kafka { bootstrap_servers => "" codec => json consumer_threads => 3 topics => ["messages","secure","pgsql_query_message"] } }

    output { elasticsearch { hosts => [ "elastic-es-internal-http:9200" ] user => "elastic" password => "1S7b73W29C0eExAqjB7J5B0O" index => "k8s-%{[kubernetes][labels][logIndex]}-%{+YYYY.MM}" } stdout { codec => rubydebug } 
            if "pgsql" in [tags] {
              elasticsearch {
                hosts => ""
                index => "pgsql-query-%{+YYYY.MM}"
                user => ""
                password => ""
              }
            }
    }
    
然后在 elasticsearch 中找到该索引
```