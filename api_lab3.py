import asyncio
import json
import logging
from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from clickhouse_driver import Client
import time

from config import CLICKHOUSE_HOST


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


class ClickHouseHandler(logging.Handler):
    def __init__(self, host, database,
                 table_info, table_warning,
                 table_error, user='default',
                 password=''):
        super().__init__()
        self.client = Client(host=host, user=user, port=9000, password=password, database=database)
        self.table_info = table_info
        self.table_warning = table_warning
        self.table_error = table_error

    def emit(self, record):
        request = record.getMessage().replace("'", '"')
        request = json.loads(request[request.find("{"):].strip())
        status_code = request['status_code']
        response_time = request['process_time']
        user_host = request['client']
        url = request['url']
        method = request['method']
        record_created_datetime = datetime.fromtimestamp(record.created)
        try:
            if record.levelno == logging.INFO:
                self.client.execute(
                    f'INSERT INTO {self.table_info} (status_code, user_host, url, time, method, response_time) VALUES',
                    [(status_code, user_host, url, record_created_datetime, method, response_time)]
                )
            elif record.levelno == logging.WARNING:
                message = request['message']
                self.client.execute(
                    f'INSERT INTO {self.table_warning} (status_code, user_host, url, time, method, response_time, message) VALUES ',
                    [(status_code, user_host, url, record_created_datetime, method, response_time, message)]
                )
            elif record.levelno == logging.ERROR:
                message = request['message']
                self.client.execute(
                    f'INSERT INTO {self.table_error} (status_code, user_host, url, time, method, response_time, message) VALUES',
                    [(status_code, user_host, url, record_created_datetime, method, response_time, message)]
                )

        except Exception as e:
            print(f"Failed to log to ClickHouse: {e}")


clickhouse_handler = ClickHouseHandler(
    host=CLICKHOUSE_HOST,
    database='logs_db',
    table_info='logs_info',
    table_error='logs_error',
    table_warning='logs_warning'
)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
clickhouse_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(clickhouse_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        log_details = {
            'method': request.method,
            'url': request.url.path,
            'status_code': response.status_code,
            'process_time': process_time,
            'client': request.client.host
        }
        print("TMTPT TRJ ")
        if 200 <= response.status_code < 400:
            logger.info(f"Request: {log_details}")
        elif 400 <= response.status_code < 500:
            try:
                log_details["message"] = await request.json()
            except json.decoder.JSONDecodeError:
                log_details["message"] = "None"
            logger.warning(f"Request: {log_details}")
        elif 500 <= response.status_code < 600:
            log_details["message"] = "None"
            logger.error(f"Request: {log_details}")

        return response
