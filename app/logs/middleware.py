from app.logs.logger import logger
from fastapi import Request, Response
import time
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict

# async def log_middleware(request: Request, call_next):
#     start = time.time()

#     response = await call_next(request)

#     end = time.time()
#     process_time = end - start

#     log_dict = {
#         'url': request.url,
#         'method': request.method,
#         'process_time': process_time,
#         # 'headers': request.headers
#     }
#     logger.info(log_dict)
    
#     return response


period = 1 #sec
period_count = 1000 #count

period_time = period / period_count # it means 10 request per second

class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app, dispatch)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message:str):
        logger.info(message)
    
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        start_time = time.time()

        if start_time - self.rate_limit_records[client_ip] < period_time:
            await self.log_message(f"Rate limit exceeded for {client_ip}")
            return Response("Rate limit exceeded", status_code=429)

        self.rate_limit_records[client_ip] = start_time

        response = await call_next(request)

        end_time = time.time()
        process_time = end_time - start_time

        log_dict = {
            'url': request.url,
            'method': request.method,
            'process_time': process_time,
            # 'headers': request.headers
        }
        logger.info(log_dict)
        
        return response