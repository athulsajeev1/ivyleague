from app.db.session import engine, Base
from app.models.models import User, Profile, Opportunity, Post, Comment, Achievement

def init_db():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    init_db()
