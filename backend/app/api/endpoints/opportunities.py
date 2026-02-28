from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Opportunity, User, Profile
from app.schemas.schemas import Opportunity as OpportunitySchema
from app.services.scraper import scraper_service
from app.services.intelligence import intelligence_engine

router = APIRouter()

@router.get("/", response_model=List[OpportunitySchema])
def get_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).all()

@router.post("/sync")
def sync_opportunities():
    count = scraper_service.sync_all()
    return {"message": f"Successfully synced {count} new opportunities."}

@router.get("/matched/{user_id}")
def get_matched_opportunities(user_id: int, db: Session = Depends(get_db)):
    user_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    opportunities = db.query(Opportunity).all()
    results = []
    
    for opp in opportunities:
        # Combine profile interests and extracted CV skills for a holistic match
        profile_data = f"{user_profile.interests or ''} {user_profile.skills or ''}".strip()
        score = intelligence_engine.calculate_match_score(
            profile_data, 
            f"{opp.title} {opp.description}"
        )
        results.append({
            "opportunity": opp,
            "match_score": score
        })
    
    # Sort by match score descending
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:10]
