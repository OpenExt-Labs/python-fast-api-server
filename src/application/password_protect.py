from fastapi import Depends, HTTPException, Query
import os
from dotenv import load_dotenv

load_dotenv('.env.local')

def verify_password(p: str = Query(..., description="Password required")):
    correct_password = os.getenv("PROFILER_SECRET_P")
    if p != correct_password:
        raise HTTPException(status_code=403, detail="Forbidden")

def get_interval(interval: int = Query(2, description="Time interval in seconds")):
    if interval < 1:
        raise HTTPException(status_code=400, detail="Interval must be at least 1 second")
    return interval