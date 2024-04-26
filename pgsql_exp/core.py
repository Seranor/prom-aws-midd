import psycopg2
from config.settings import *
from pgsql_exp.metrics_name import *


# 建立数据库连接
def create_db_connection():
    conn = psycopg2.connect(
        host=PG_DATABASE,
        port=PG_PORT,
        database=PG_DBNAME,
        user=PG_USER,
        password=PG_PWD
    )
    return conn


# pgsql 连接数 查询并更新指标
def pg_connections_query(conn):
    cursor = conn.cursor()
    query = """
        SELECT count(*) AS total_connections,
               sum(case when state = 'active' then 1 else 0 end) AS active_connections,
               sum(case when state = 'idle' then 1 else 0 end) AS idle_connections
        FROM pg_stat_activity;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    total_conn_count = result[0]
    active_conn_count = result[1]
    idle_conn_count = result[2]
    # 总连接数
    pg_total_connections.set(total_conn_count)
    # 活动连接数
    pg_active_connections.set(active_conn_count)
    # 空闲连接数
    pg_idle_connections.set(idle_conn_count)
    cursor.close()


# pgsql db size 查询并更新指标 单位是字节
def db_size_query(conn):
    cursor = conn.cursor()
    query = """
        SELECT datname AS database_name, pg_database_size(datname) AS database_size_bytes
        FROM pg_database
        WHERE datistemplate = false
        ORDER BY pg_database_size(datname) DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        database_name = row[0]
        database_size_bytes_value = row[1]
        pg_database_size_bytes.labels(database_name=database_name).set(float(database_size_bytes_value))
    cursor.close()


def pg_connection_count_query(conn):
    cursor = conn.cursor()
    query = """
        SELECT usename AS username, count(*) AS connection_count
        FROM pg_stat_activity
        GROUP BY usename;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        username = row[0]
        count = row[1]
        pg_user_connection_count.labels(username=username).set(count)
    cursor.close()


# 启动时间 查询并更新指标
def pg_uptime_query(conn):
    cursor = conn.cursor()
    query = """
        SELECT pg_postmaster_start_time() AS postmaster_start_time,
               EXTRACT(EPOCH FROM (current_timestamp - pg_postmaster_start_time())) AS uptime_seconds;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    uptime_seconds_value = result[1]
    pg_uptime_seconds.set(float(uptime_seconds_value))
    cursor.close()


# 查询 QPS all read write
def pg_qps_query(conn):
    cursor = conn.cursor()
    query = """
        with
        a as (select sum(calls) s, sum(case when ltrim(query,' ') ~* '^select' then calls else 0 end) q from pg_stat_statements),
        b as (select sum(calls) s, sum(case when ltrim(query,' ') ~* '^select' then calls else 0 end) q from pg_stat_statements , pg_sleep(1))
        select
        b.s-a.s AS QPS,
        b.q-a.q AS read,   
        b.s-b.q-a.s+a.q AS write
        from a,b;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    pg_qps_all_value = result[0]
    pg_qps_read_value = result[1]
    pg_qps_write_value = result[2]
    pg_qps_all.set(pg_qps_all_value)
    pg_qps_read.set(pg_qps_read_value)
    pg_qps_write.set(pg_qps_write_value)
    cursor.close()


def pg_wait_session_query(conn):
    cursor = conn.cursor()
    query1 = """
        select count(*) from pg_stat_activity where wait_event_type is not null;
    """
    query2 = """
        select count(*) from pg_stat_activity where wait_event_type is not null and now()-state_change > interval '5 second';
    """
    cursor.execute(query1)
    res1 = cursor.fetchone()
    pg_wait_session_sec.set(res1[0])
    cursor.execute(query2)
    res2 = cursor.fetchone()
    pg_wait_session_five_sec.set(res2[0])
    cursor.close()


# 查询 慢语句的详细信息
def pg_slow_sql_query(conn):
    cursor = conn.cursor()
    query = """
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
    """
    cursor.execute(query)
    # 处理查询结果并导出为Prometheus指标

    for row in cursor.fetchall():
        query = row[0]
        calls = row[1]
        total_exec_time = row[2]
        min_exec_time = row[3]
        max_exec_time = row[4]
        mean_exec_time = row[5]
        blk_read_time = row[6]
        blk_write_time = row[7]
        rows = row[8]
        hit_percent = row[9]
        query = query.replace(" ", "")

        if hit_percent is None:
            hit_percent = 0

        # 设置指标的值
        pg_query_calls.labels(query=query).set(float(calls))
        pg_query_total_exec_time.labels(query=query).set(float(total_exec_time))
        pg_query_min_exec_time.labels(query=query).set(float(min_exec_time))
        pg_query_max_exec_time.labels(query=query).set(float(max_exec_time))
        pg_query_mean_exec_time.labels(query=query).set(float(mean_exec_time))
        pg_query_blk_read_time.labels(query=query).set(float(blk_read_time))
        pg_query_blk_write_time.labels(query=query).set(float(blk_write_time))
        pg_query_rows.labels(query=query).set(int(rows))
        pg_query_hit_percent.labels(query=query).set(hit_percent)
    cursor.close()