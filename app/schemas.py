from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# Metric

class MetricBase(BaseModel):
    name: str
    value: float
    unit: Optional[str] = None
    time: Optional[datetime] = None


class MetricCreate(MetricBase):
    pass


class MetricRead(MetricBase):
    metric_id: int

    class Config:
        orm_mode = True


# Campaign

class CampaignBase(BaseModel):
    name: str
    objective: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = "DRAFT"


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    objective: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class CampaignRead(CampaignBase):
    campaign_id: int

    class Config:
        orm_mode = True


# Channel

class ChannelBase(BaseModel):
    type: str
    name: str
    handle: Optional[str] = None
    external_id: Optional[str] = None


class ChannelCreate(ChannelBase):
    pass


class ChannelRead(ChannelBase):
    channel_id: int

    class Config:
        orm_mode = True


# Analytics report

class AnalyticsReportBase(BaseModel):
    scope: str
    generated_at: Optional[datetime] = None
    insights: Optional[str] = None


class AnalyticsReportCreate(AnalyticsReportBase):
    campaign_id: int
    metrics: List[MetricCreate] = []


class AnalyticsReportRead(AnalyticsReportBase):
    report_id: int
    campaign_id: int
    metrics: List[MetricRead] = []

    class Config:
        orm_mode = True
