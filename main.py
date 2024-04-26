import threading
from prometheus_client import start_http_server
from config.settings import *
from pgsql_exp.pg_exporter import main_loop_pg_exporter
from pgsql_exp.aws_pg_exporter import main_loop_aws_pg_exporter
from mongo_exp.mongo_exporter import main_loop_mongo_exporter
from mongo_exp.aws_mongo_exporter import main_loop_aws_mongo_exporter
from redis_exp.aws_redis_exporter import main_loop_aws_redis_exporter

if __name__ == '__main__':
    # 启动 Prometheus HTTP 服务器
    start_http_server(SERVER_PORT)  # 替换为您希望的端口号
    # # 多线程运行
    thread_pg_export = threading.Thread(target=main_loop_pg_exporter)
    thread_aws_pg_export = threading.Thread(target=main_loop_aws_pg_exporter)
    thread_mongo_export = threading.Thread(target=main_loop_mongo_exporter)
    thread_aws_mongo_export = threading.Thread(target=main_loop_aws_mongo_exporter)
    thread_aws_redis_export = threading.Thread(target=main_loop_aws_redis_exporter)

    thread_pg_export.start()
    thread_aws_pg_export.start()
    thread_mongo_export.start()
    thread_aws_mongo_export.start()
    thread_aws_redis_export.start()

    thread_pg_export.join()
    thread_aws_pg_export.join()
    thread_mongo_export.join()
    thread_aws_mongo_export.join()
    thread_aws_redis_export.join()
