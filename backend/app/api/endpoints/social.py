from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Post, Comment, User, post_likes
from app.schemas.schemas import Post as PostSchema, PostBase, CommentBase, Comment as CommentSchema

router = APIRouter()

@router.get("/", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    # Add manual likes count for now, in a real app this would be optimized
    for post in posts:
        post.likes_count = len(post.likes)
    return posts

@router.post("/", response_model=PostSchema)
def create_post(post_in: PostBase, user_id: int, db: Session = Depends(get_db)):
    new_post = Post(content=post_in.content, author_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.post("/{post_id}/like")
def like_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not post or not user:
        raise HTTPException(status_code=404, detail="Post or User not found")
    
    if user in post.likes:
        post.likes.remove(user)
        message = "Unliked"
    else:
        post.likes.append(user)
        message = "Liked"
    
    db.commit()
    return {"message": message}

@router.post("/{post_id}/comments", response_model=CommentSchema)
def add_comment(post_id: int, comment_in: CommentBase, user_id: int, db: Session = Depends(get_db)):
    new_comment = Comment(content=comment_in.content, post_id=post_id, author_id=user_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
