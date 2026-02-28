from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, Profile, Opportunity
from app.services.auto_app import auto_app_service

router = APIRouter()

@router.post("/resume/upload")
async def upload_resume(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    file_path = auto_app_service.save_resume(user_id, file)
    profile.resume_url = file_path
    
    # Extract info automatically to update profile
    extracted = auto_app_service.extract_info_from_pdf(file_path)
    if "error" not in extracted:
        profile.skills = extracted["skills"]
        # Boost InCoScore based on extracted skills for visual impact
        skill_count = len(extracted["skills"].split(','))
        profile.incoscore += (skill_count * 15) # Reward for each extracted skill
        profile.incoscore = min(profile.incoscore, 999) # Cap at 999
    
    db.commit()
    return {"message": "Resume processed successfully.", "extracted_data": extracted}

@router.get("/autofill/{user_id}/{opp_id}")
def get_autofill_data(user_id: int, opp_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    opportunity = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
    
    if not profile or not opportunity:
        raise HTTPException(status_code=404, detail="User or Opportunity not found")
    
    form_data = auto_app_service.autofill_form(profile, opportunity)
    return form_data
