import time
from pgsql_exp.core import *


# 主循环
def main_loop_pg_exporter():
    slow_sql_timer = time.time()  # 初始化计时器
    while True:
        try:
            conn = create_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.fetchone()
            pg_up.set(int(1))
            pg_connections_query(conn)
            db_size_query(conn)
            pg_connection_count_query(conn)
            pg_uptime_query(conn)
            pg_qps_query(conn)
            pg_wait_session_query(conn)

            # 每60秒执行一次pg_slow_sql_query(conn)
            if time.time() - slow_sql_timer >= 60:
                pg_slow_sql_query(conn)
                slow_sql_timer = time.time()  # 重置计时器

            time.sleep(30)
        except (psycopg2.Error, Exception) as e:
            print(e)
            pg_up.set(int(0))
            time.sleep(30)
