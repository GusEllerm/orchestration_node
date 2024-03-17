from fastapi import FastAPI, Request, Depends
from login import router as login_router
from logs import router as logs_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import uvicorn
import logging
import datetime

from login import is_user_logged_in
from orchestration_logic.gladier_flow import run_flow
from logs import configure_logs, uvicorn_log_config

# Scheduler for (eventual) polling of data sources
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup procedures before the YIELD
    # On shutdown procedures after teh YIELD
    scheduler.start()
    startup_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Orchestration Server is starting up at {startup_time}")
    logging.info(f"Scheduler started at {startup_time}")  
    yield
    shutdown_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Orchestration Server is shutting down at {shutdown_time}")
    
# Create the app instance, connect modules, mount static and template files
app = FastAPI(lifespan=lifespan) 
app.include_router(login_router)
app.include_router(logs_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @scheduler.scheduled_job(CronTrigger(minute='*'))  
# async def scheduled_job():
#     """
#     Scheduler will eventually enable periodic checking for new 
#     avaliable data. On new data, execute a LivePublication flow.
#     Currently set to run every minute for testing.
#     """
#     await test_execution()
    
@app.get("/")
def read_root(request: Request, user: str = Depends(is_user_logged_in)):
    return templates.TemplateResponse("control_center.html", {"request": request})

@app.get("/test")
async def test_execution():
    execution_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Starting test execution of globus flow {execution_time}")
    # Only uncomment this if you know what you are doing!
    await execute_globus_flow()
    completion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": f"Test execution of Globus Flow completed at {completion_time}"}

async def execute_globus_flow():
    # Your code to execute the Globus Flow
    logging.info("Executing Globus Flow")
    run_flow()

# A hackity hackity hack hack to remove the polling 
# logs for hitting the /logs/ api when updating the 
# control center. 
@app.middleware("http")
async def suppress_log_middleware(request: Request, call_next):
    # Check if the request path starts with /logs/
    if request.url.path.startswith("/logs/"):
        # Temporarily disable the uvicorn.access logger
        access_logger = logging.getLogger("uvicorn.access")
        original_level = access_logger.level
        access_logger.setLevel(logging.CRITICAL)
        response = await call_next(request)
        # Restore the original log level of the uvicorn.access logger
        access_logger.setLevel(original_level)
        return response
    return await call_next(request)

if __name__ == "__main__":
    # Configure logs
    configure_logs()
    # Start up Server
    uvicorn.run(
        app, 
        host="0.0.0.0", port=8080, 
        log_config=uvicorn_log_config
    )