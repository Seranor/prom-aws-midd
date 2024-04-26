import time
from mongo_exp.core import *


# mongo 主循环
def main_loop_mongo_exporter():
    while True:
        try:
            client = create_mongodb_connection()
            basic_monitor(client)
            mongo_up.set(1)
            time.sleep(60)
        except:
            print("error mongo conn")
            mongo_up.set(0)
            time.sleep(60)
