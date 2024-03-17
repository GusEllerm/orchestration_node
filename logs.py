from fastapi import APIRouter
from fastapi.responses import JSONResponse
from uvicorn.logging import DefaultFormatter
import logging
import os
import re

router = APIRouter()

def configure_logs():
    # Configure logging o-server
    logging.basicConfig(
        filename='logs/o-server.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def read_log_file(file_path):
    if os.path.exists(file_path):
        num_lines = 30
        with open(file_path, "r") as file:
            lines = file.readlines()
            last_lines = lines[-num_lines:] if len(lines) > num_lines else lines
            # Regular expression to match everything before the log level
            preamble_pattern = re.compile(r"^.*?(INFO|ERROR|WARNING|DEBUG) - ")
            # Remove the preamble from each line, keeping only the log level and the message
            cleaned_lines = [preamble_pattern.sub(r"\1 - ", line) for line in last_lines]
            return "<br>".join(cleaned_lines)
    else:
        return "Log file not available."

# Endpoints for serving log data
@router.get("/logs/server")
def get_server_log():
    log_content = read_log_file("logs/o-server.log")
    return JSONResponse(content={"log": log_content})

@router.get("/logs/oLogic")
def get_oLogic_log():
    log_content = read_log_file("logs/orchestration_logic.log")
    return JSONResponse(content={"log": log_content})

@router.get("/logs/uvicorn")
def get_uvicorn_log():
    log_content = read_log_file("logs/uvicorn.log")
    return JSONResponse(content={"log": log_content})

uvicorn_log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/uvicorn.log",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
