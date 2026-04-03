import psycopg2
from config import db_config

def get_connection():
    return psycopg2.connect(**db_config)