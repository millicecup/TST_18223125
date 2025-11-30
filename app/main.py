from fastapi import FastAPI

from .database import Base, engine
from .routers import campaigns, channels, reports, auth, campaign_links, posts, goals, dashboards

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Learnova Tracker & Analytics API")

app.include_router(campaigns.router)
app.include_router(channels.router)
app.include_router(reports.router)
app.include_router(auth.router)
app.include_router(campaign_links.router)
app.include_router(posts.router)
app.include_router(goals.router)
app.include_router(dashboards.router)