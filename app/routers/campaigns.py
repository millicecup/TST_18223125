from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..routers.auth import get_current_user
router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("/", response_model=schemas.CampaignRead)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    campaign = models.Campaign(**payload.dict())
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/", response_model=list[schemas.CampaignRead])
def list_campaigns(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Campaign).all()


@router.get("/{campaign_id}", response_model=schemas.CampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.patch("/{campaign_id}", response_model=schemas.CampaignRead)
def update_campaign(
    campaign_id: int,
    payload: schemas.CampaignUpdate,
    db: Session = Depends(get_db),
):
    campaign = db.query(models.Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}", status_code=204)
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return
