from fastapi import APIRouter
from app.api.endpoints import auth, opportunities, social, dashboard, profile, chat

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
router.include_router(social.router, prefix="/social", tags=["social"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(profile.router, prefix="/profile", tags=["profile"])
router.include_router(chat.router, tags=["chat"])
