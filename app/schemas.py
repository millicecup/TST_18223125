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


# user
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class CampaignLinkBase(BaseModel):
    campaign_id: int
    url_original: str
    url_short: Optional[str] = None
    utm: Optional[str] = None


class CampaignLinkCreate(CampaignLinkBase):
    pass


class CampaignLinkRead(CampaignLinkBase):
    link_id: int

    model_config = {
        "from_attributes": True
    }

class PostBase(BaseModel):
    channel_id: int
    external_id: Optional[str] = None
    url: Optional[str] = None
    posted_at: Optional[datetime] = None
    caption: Optional[str] = None
    media_type: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    post_id: int

    class Config:
        orm_mode = True


class GoalBase(BaseModel):
    campaign_id: int
    name: str
    kpi: str
    target_value: Optional[float] = None
    period: Optional[str] = None


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    goal_id: int

    class Config:
        orm_mode = True


class DashboardBase(BaseModel):
    org_id: Optional[str] = None
    name: str
    layout: Optional[str] = None


class DashboardCreate(DashboardBase):
    pass


class DashboardRead(DashboardBase):
    dashboard_id: int
    class Config:
        orm_mode = True