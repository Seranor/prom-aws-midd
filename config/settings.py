from dotenv import load_dotenv
import os
import json

load_dotenv()
PG_DATABASE = os.getenv('PG_DATABASE')
PG_PORT = os.getenv('PG_PORT')
PG_USER = os.getenv('PG_USER')
PG_PWD = os.getenv('PG_PWD')
PG_DBNAME = os.getenv('PG_DBNAME')
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_RDS_INSTANCE_ID = os.getenv('AWS_RDS_INSTANCE_ID')
AWS_RDS_TYPE = os.getenv('AWS_RDS_TYPE')
SERVER_PORT = int(os.getenv("SERVER_PORT"))
if SERVER_PORT is None:
    SERVER_PORT = 9010

MONGO_INFO = json.loads(os.getenv("MONGO_INFO"))
AWS_MONGO_INSTANCE_INFO = json.loads(os.getenv("AWS_MONGO_INSTANCE_INFO"))
AWS_ELASTICACHE_INSTANCE_INFO = json.loads(os.getenv("AWS_ELASTICACHE_INSTANCE_INFO"))

# AWS_MONGO_INSTANCE_ID = os.getenv('AWS_MONGO_INSTANCE_ID')
# AWS_MONGO_TYPE = os.getenv('AWS_MONGO_TYPE')
# KAFKA_SERVER = os.getenv('KAFKA_SERVER')
# PG_ENV_NAME = os.getenv('PG_ENV_NAME')