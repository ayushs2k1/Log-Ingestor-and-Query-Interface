
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from utils.loggingConfig import logger
from fastapi import HTTPException

class LogRequestDTO(BaseModel):
    level: str
    message: str
    resourceId: str
    timestamp: datetime
    traceId: str
    spanId: str
    commit: str
    metadata: dict


async def validatePayload(payload):
    try:
        LogRequestObject = LogRequestDTO(**payload)
        return LogRequestObject
    except ValidationError as e:
        logger.error(f"Bad Request: payload is not valid")
        raise HTTPException(status_code=400, detail="Bad Request")

