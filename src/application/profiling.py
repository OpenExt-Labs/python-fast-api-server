import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict
from collections import defaultdict
import threading

# Use a lock for thread-safe operation
lock = threading.Lock()

profile_data: Dict[str, Dict] = defaultdict(lambda: {
    'total_requests': 0,
    'total_time': 0.0,
    'last_time': 0.0,
    'processing_rate': 0.0,
    'avg_time': 0.0
})

class ProfilingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        endpoint_name = request.url.path

        # Lock the section where data is modified to ensure thread safety
        with lock:
            data = profile_data[endpoint_name]
            data['total_requests'] += 1
            data['total_time'] += process_time
            data['last_time'] = process_time
            data['avg_time'] = data['total_time'] / data['total_requests']
            if process_time > 0:
                # Calculate processing rate as number of requests per second
                data['processing_rate'] = 1 / process_time
            else:
                data['processing_rate'] = float('inf')

        return response

