from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class CampaignStatusEnum(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    objective = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="DRAFT")

    links = relationship("CampaignLink", back_populates="campaign")
    goals = relationship("Goal", back_populates="campaign")
    reports = relationship("AnalyticsReport", back_populates="campaign")


class CampaignLink(Base):
    __tablename__ = "campaign_links"

    link_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id"))
    url_original = Column(String, nullable=False)
    url_short = Column(String, nullable=True)
    utm = Column(String, nullable=True)

    campaign = relationship("Campaign", back_populates="links")


class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)   # instagram, youtube, tiktok
    name = Column(String, nullable=False)
    handle = Column(String, nullable=True)
    external_id = Column(String, nullable=True)

    posts = relationship("Post", back_populates="channel")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    external_id = Column(String, nullable=True)
    url = Column(String, nullable=True)
    posted_at = Column(DateTime, nullable=True)
    caption = Column(Text, nullable=True)
    media_type = Column(String, nullable=True)

    channel = relationship("Channel", back_populates="posts")


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id"))
    name = Column(String, nullable=False)
    kpi = Column(String, nullable=False)
    target_value = Column(Float, nullable=True)
    period = Column(String, nullable=True)

    campaign = relationship("Campaign", back_populates="goals")


class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"

    report_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id"))
    scope = Column(String, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    insights = Column(Text, nullable=True)

    campaign = relationship("Campaign", back_populates="reports")
    metrics = relationship("Metric", back_populates="report")


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("analytics_reports.report_id"))
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    time = Column(DateTime, default=datetime.utcnow)

    report = relationship("AnalyticsReport", back_populates="metrics")


class Dashboard(Base):
    __tablename__ = "dashboards"

    dashboard_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    layout = Column(Text, nullable=True)
