from pymongo import MongoClient
from config.settings import MONGO_INFO
from mongo_exp.metrics_name import *


# 建立mongo 连接
def create_mongodb_connection():
    connect_info = MONGO_INFO["connect"]
    parameter_info = MONGO_INFO["parameter"]

    connection_string = "mongodb://{user}:{pwd}@{address}:{port}/?authSource={authSource}&tls={tls}&tlsCAFile={tlsCAFile}&replicaSet={replicaSet}&readPreference={readPreference}&retryWrites={retryWrites}".format(
        user=connect_info['user'],
        pwd=connect_info['pwd'],
        address=connect_info['address'],
        port=connect_info['port'],
        authSource=parameter_info['authSource'],
        tls=parameter_info['tls'],
        tlsCAFile=parameter_info['tlsCAFile'],
        replicaSet=parameter_info['replicaSet'],
        readPreference=parameter_info['readPreference'],
        retryWrites=parameter_info['retryWrites']
    )

    # 连接到 MongoDB
    client = MongoClient(connection_string)
    return client


def basic_monitor(conn):
    db_admin = conn.admin
    server_status = db_admin.command('serverStatus')

    # 总信息
    # print(server_status)

    mongo_version.info({'version': str(server_status['version'])})
    mongo_uptime_seconds.set(server_status['uptime'])
    mongo_current_connections.set(server_status['connections']['current'])
    mongo_available_connections.set(server_status['connections']['available'])
    mongo_totalCreated_connections.set(server_status['connections']['totalCreated'])
    mongo_opcounters_insert.set(server_status['opcounters']['insert'])
    mongo_opcounters_query.set(server_status['opcounters']['query'])
    mongo_opcounters_update.set(server_status['opcounters']['update'])
    mongo_opcounters_delete.set(server_status['opcounters']['delete'])
    mongo_opcounters_getmore.set(server_status['opcounters']['getmore'])
    mongo_opcounters_command.set(server_status['opcounters']['command'])
    mongo_document_deleted.set(server_status['metrics']['document']['deleted'])
    mongo_document_inserted.set(server_status['metrics']['document']['inserted'])
    mongo_document_returned.set(server_status['metrics']['document']['returned'])
    mongo_document_updated.set(server_status['metrics']['document']['updated'])

    conn.close()


'''
db.serverStatus()
db.adminCommand({'replSetGetStatus': 1})
'''

# client = create_mongodb_connection()
# basic_monitor(client)

# if __name__ == '__main__':
#     start_http_server(9090)
#     while True:
#         client = create_mongodb_connection()
#         basic_monitor(client)
#         time.sleep(10)
