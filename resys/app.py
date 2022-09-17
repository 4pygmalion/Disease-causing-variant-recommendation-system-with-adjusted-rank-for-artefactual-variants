import os
import sys
from fastapi import FastAPI

ASC3_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ASC3_DIR)

from routers import api_router

api = FastAPI()
api.include_router(api_router)
