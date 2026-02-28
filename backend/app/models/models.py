from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# Many-to-many relationship for likes
post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    
    profile = relationship("Profile", back_populates="user", uselist=False)
    posts = relationship("Post", back_populates="author")
    achievements = relationship("Achievement", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skills = Column(Text)  # Comma-separated or JSON string
    interests = Column(Text)
    resume_url = Column(String, nullable=True)
    incoscore = Column(Integer, default=0)
    
    user = relationship("User", back_populates="profile")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    url = Column(String)
    source = Column(String)
    domain = Column(String)  # Classified by AI: Law, AI, Bio, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author = relationship("User", back_populates="posts")
    likes = relationship("User", secondary=post_likes)
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    post = relationship("Post", back_populates="comments")

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String) # Hackathon, Internship, Research, etc.
    title = Column(String)
    date = Column(DateTime)
    
    user = relationship("User", back_populates="achievements")
