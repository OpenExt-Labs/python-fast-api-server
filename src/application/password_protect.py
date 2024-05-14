from fastapi import Depends, HTTPException, Query

def verify_password(p: str = Query(..., description="Password required")):
    correct_password = "876893"
    if p != correct_password:
        raise HTTPException(status_code=403, detail="Forbidden")

def get_interval(interval: int = Query(2, description="Time interval in seconds")):
    if interval < 1:
        raise HTTPException(status_code=400, detail="Interval must be at least 1 second")
    return interval