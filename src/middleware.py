import time

from fastapi import Request

from main import app
from logger import log


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log(log.INFO, "Time estimated - [%s]", process_time)
    return response
