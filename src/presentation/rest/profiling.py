from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from src.application.password_protect import verify_password, get_interval
from src.application.profiling import profile_data

router = APIRouter(prefix="/profilers", tags=["Profilers"])

templates = Jinja2Templates(directory="src/templates")

@router.get("", status_code=200, dependencies=[Depends(verify_password)])
async def get_profilers(request: Request, interval: int = Depends(get_interval)):
    rounded_data = {}
    for endpoint, metrics in profile_data.items():
        rounded_data[endpoint] = {
            'total_requests': metrics['total_requests'],
            'total_time': round(metrics['total_time'] * 1000, 2),
            'last_time': round(metrics['last_time'] * 1000, 2),
            'avg_time': round(metrics['avg_time'] * 1000, 2),
            'processing_rate': round(metrics['processing_rate'], 2) if metrics['processing_rate'] != float('inf') else float('inf'),
            'interval': interval  # Adding interval to context if needed
        }
    context = {"request": request, "profile_data": rounded_data, "enumerate": enumerate, "interval": interval}
    return templates.TemplateResponse("profilers.html", context)
