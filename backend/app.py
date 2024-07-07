from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from routes import router
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.include_router(router)


templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create_building")
async def get_create_building(request: Request):
    return templates.TemplateResponse("create_building.html", {"request": request})

@app.get("/building_details")
async def get_building_details(request: Request):
    return templates.TemplateResponse("building_details.html", {"request": request})

@app.get("/building_analysis")
async def get_building_analysis(request: Request):
    return templates.TemplateResponse("building_analysis.html", {"request": request})
