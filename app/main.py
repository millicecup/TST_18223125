from fastapi import FastAPI

from .database import Base, engine
from .routers import campaigns, channels, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learnova Tracker & Analytics API")

app.include_router(campaigns.router)
app.include_router(channels.router)
app.include_router(reports.router)
