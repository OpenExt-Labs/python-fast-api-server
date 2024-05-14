from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from src.application.authentication.dependency_injection import get_current_user
from src.domain.users.models import User
from src.application.profiling import profile_data

router = APIRouter(prefix="/profilers", tags=["Profilers"])

templates = Jinja2Templates(directory="src/templates")

@router.get("", status_code=200)
async def get_profilers(request: Request):
    rounded_data = {}
    for endpoint, metrics in profile_data.items():
        rounded_data[endpoint] = {
            'total_requests': metrics['total_requests'],
            'total_time': round(metrics['total_time'] * 1000, 2),
            'last_time': round(metrics['last_time'] * 1000, 2),
            'avg_time': round(metrics['avg_time'] * 1000, 2),
            'processing_rate': round(metrics['processing_rate'], 2) if metrics['processing_rate'] != float('inf') else float('inf')
        }
    context = {"request": request, "profile_data": rounded_data, "enumerate": enumerate}
    return templates.TemplateResponse("profilers.html", context)
