'''
每个库的大小  需要 progress 用户
SELECT datname AS database_name, pg_database_size(datname) AS database_size_bytes
FROM pg_database
WHERE datistemplate = false
ORDER BY pg_database_size(datname) DESC;

每个用户对应的连接数情况
SELECT usename AS username, count(*) AS connection_count
FROM pg_stat_activity
GROUP BY usename;

总连接数 (total_connections)、活动连接数 (active_connections) 和空闲连接数 (idle_connections)
SELECT count(*) AS total_connections,
       sum(case when state = 'active' then 1 else 0 end) AS active_connections,
       sum(case when state = 'idle' then 1 else 0 end) AS idle_connections
FROM pg_stat_activity;

启动时间
SELECT pg_postmaster_start_time() AS postmaster_start_time,
       current_timestamp - pg_postmaster_start_time() AS uptime


QPS 每秒的查询数
with
a as (select sum(calls) s, sum(case when ltrim(query,' ') ~* '^select' then calls else 0 end) q from pg_stat_statements),
b as (select sum(calls) s, sum(case when ltrim(query,' ') ~* '^select' then calls else 0 end) q from pg_stat_statements , pg_sleep(1))
select
b.s-a.s AS QPS,          -- QPS
b.q-a.q AS read,          -- 读QPS
b.s-b.q-a.s+a.q AS write   -- 写QPS
from a,b;

每秒处于等待的会话数有多少
select count(*) from pg_stat_activity where wait_event_type is not null;

每5秒处于等待的会话数有多少
select count(*) from pg_stat_activity where wait_event_type is not null and now()-state_change > interval '5 second';

慢SQL
calls 执行次数
total_exec_time  执行语句所花费的总时间（以毫秒为单位）
min_exec_time  执行语句所花费的最短时间（以毫秒为单位）
max_exec_time 执行语句所花费的最长时间
mean_exec_time  执行语句所花费的平均时间（以毫秒为单位）
rows   语句检索或影响的总行数
hit_percent  缓存命中率
blk_read_time   句读取块所花费的总时间，以毫秒为单位
blk_write_time 语句写入块所花费的总时间，以毫秒为单位

SELECT query, calls, total_exec_time, min_exec_time, max_exec_time, mean_exec_time, blk_read_time ,blk_write_time,rows,
        100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE query NOT LIKE 'BEGIN'
	AND query NOT LIKE 'COMMIT'
  AND query NOT LIKE '%pg_database_size(%'
  AND query NOT LIKE 'SET statement_timeout=%'
  AND query NOT LIKE 'SELECT 1'
ORDER BY calls DESC
LIMIT 20;


CPU 内存 存储空间 IO延迟  网络吞吐量
'''