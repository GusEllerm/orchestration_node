from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import datetime

from orchestration_logic.gladier_flow import run_flow

# Configure logging
logging.basicConfig(filename='o-server.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    
# Create the app instance with lifespan definition
app = FastAPI(lifespan=lifespan) 

@scheduler.scheduled_job(CronTrigger(minute='*'))  
async def scheduled_job():
    """
    Scheduler will eventually enable periodic checking for new 
    avaliable data. On new data, execute a LivePublication flow.
    Currently set to run every minute for testing.
    """
    await test_execution()

async def execute_globus_flow():
    # Your code to execute the Globus Flow
    logging.info("Executing Globus Flow")

    # Only uncomment this if you know what you are doing!
    # run_flow()
    
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/test")
async def test_execution():
    execution_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Starting test execution of globus flow {execution_time}")
    await execute_globus_flow()
    completion_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": f"Test execution of Globus Flow completed at {completion_time}"}
