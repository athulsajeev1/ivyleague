from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Profile Schemas
class ProfileBase(BaseModel):
    skills: str
    interests: str
    resume_url: Optional[str] = None

class Profile(ProfileBase):
    incoscore: int
    
    class Config:
        from_attributes = True

# Opportunity Schemas
class OpportunityBase(BaseModel):
    title: str
    description: str
    url: str
    source: str
    domain: str

class Opportunity(OpportunityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Social Schemas
class CommentBase(BaseModel):
    content: str

class Comment(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    content: str

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    likes_count: int = 0
    comments: List[Comment] = []
    
    class Config:
        from_attributes = True
