from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        
    def _clean_old_requests(self, client_id: str):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < 60
        ]

    async def __call__(self, request: Request):
        client_id = request.client.host
        current_time = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self._clean_old_requests(client_id)
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        self.requests[client_id].append(current_time)
        return True 