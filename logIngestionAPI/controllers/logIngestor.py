from fastapi import APIRouter, HTTPException, Body
from utils.loggingConfig import logger
from models.logRequestModel import validatePayload
from services.insertLog import retryInsertLogRecord


router = APIRouter()

@router.post("/logIngest")
async def logIngest(request: dict = Body(...)):
    logger.info(f"Request recieved : {request}")
    # Create a LogRequestDTO object
    logRequestObject = await validatePayload(request)
    logger.info(f"Valid Request")
    # Insert the log record
    if await retryInsertLogRecord(logRequestObject):
        logger.info("Log record inserted successfully")
        return {"message": "Log record inserted successfully"}
    else:
        logger.error("Failed to insert log record")
        raise HTTPException(status_code=500, detail="Failed to insert log record")
    

