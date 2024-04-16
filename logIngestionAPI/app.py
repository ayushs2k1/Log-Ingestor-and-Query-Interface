from utils.loggingConfig import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.logIngestor import router as logIngestRouter
import uvicorn


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(logIngestRouter)

@app.get("/ping")
def homepage():
    logger.info("server reponded successfully")
    return {"message" : "server responded successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)


