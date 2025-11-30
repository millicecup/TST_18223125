from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

from ..routers.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/", response_model=schemas.AnalyticsReportRead)
def create_report(payload: schemas.AnalyticsReportCreate, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).get(payload.campaign_id)
    if not campaign:
        raise HTTPException(status_code=400, detail="Campaign not found")

    report = models.AnalyticsReport(
        campaign_id=payload.campaign_id,
        scope=payload.scope,
        generated_at=payload.generated_at,
        insights=payload.insights,
    )
    db.add(report)
    db.flush()

    for metric_data in payload.metrics:
        metric = models.Metric(
            report_id=report.report_id,
            **metric_data.dict(),
        )
        db.add(metric)

    db.commit()
    db.refresh(report)
    return report

@router.get("/", response_model=list[schemas.CampaignRead])
def list_campaigns(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Campaign).all()
