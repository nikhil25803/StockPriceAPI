"""Imports"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from .db import db_config
from .routes import api_routes
from fastapi.middleware.cors import CORSMiddleware

# Connect DB
db_config.connect_db()

# Creating the app
app = FastAPI(
    title="Stock Price View Application API",
    description="An API to access and manage data from the Bombay Stock Exchange (BSE)",
    version="1",
    contact={
        "name": "Nikhil Raj",
        "url": "https://github.com/nikhil25803/StockPriceAPI",
    },
    license_info={
        "name": " MIT license",
        "url": "https://github.com/nikhil25803/StockPriceAPI/blob/main/LICENSE",
    },
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route for ping test
@app.get("/", tags=["Test"], description="Ping Test")
async def ping_test():
    return JSONResponse(
        content={"messgae": "Server is up and running.", "status": status.HTTP_200_OK},
        status_code=200,
    )


# Include Routers
app.include_router(api_routes.router)
