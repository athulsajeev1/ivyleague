from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import User, Profile
from app.schemas.schemas import User as UserSchema

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    # Join User with Profile and sort by InCoScore
    results = db.query(User, Profile).join(Profile).order_by(Profile.incoscore.desc()).limit(10).all()
    
    leaderboard = []
    for user, profile in results:
        leaderboard.append({
            "id": user.id,
            "full_name": user.full_name,
            "incoscore": profile.incoscore,
            "skills": profile.skills
        })
    return leaderboard

@router.get("/profile/{user_id}")
def get_student_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    
    return {
        "user": user,
        "profile": user.profile,
        "achievements": user.achievements
    }
