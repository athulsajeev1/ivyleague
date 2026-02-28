from app.db.session import SessionLocal, engine, Base
from app.models.models import User, Profile, Opportunity, Post, Achievement
from app.core.security import get_password_hash
from datetime import datetime

def seed_db():
    db = SessionLocal()
    
    # 1. Create Scholar Community
    scholars = [
        {"email": "demo@ivy.edu", "name": "Jonathan Harvard", "score": 750, "skills": "Python, Data Science", "interests": "AI, Robotics"},
        {"email": "clara@princeton.edu", "name": "Clara Princeton", "score": 890, "skills": "Macroeconomics, Policy", "interests": "Public Policy"},
        {"email": "marcus@stanford.edu", "name": "Marcus Stanford", "score": 920, "skills": "React, TypeScript, UI/UX", "interests": "Human-Computer Interaction"},
        {"email": "elena@yale.edu", "name": "Elena Yale", "score": 840, "skills": "International Law, Ethics", "interests": "Human Rights"},
        {"email": "wei@mit.edu", "name": "Wei Zhang", "score": 960, "skills": "Quantum Computing, Physics", "interests": "Deep Tech"},
        {"email": "sarah@oxford.edu", "name": "Sarah Oxford", "score": 780, "skills": "Digital Humanities, History", "interests": "Arts"}
    ]

    for s in scholars:
        user = db.query(User).filter(User.email == s["email"]).first()
        if not user:
            print(f"Seeding {s['name']}...")
            user = User(
                email=s["email"],
                hashed_password=get_password_hash("password123"),
                full_name=s["name"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            profile = Profile(
                user_id=user.id,
                skills=s["skills"],
                interests=s["interests"],
                incoscore=s["score"]
            )
            db.add(profile)
            
            # Add a generic achievement
            ach = Achievement(user_id=user.id, category="Scholarship", title=f"Excellence in {s['interests']}")
            db.add(ach)
            db.commit()

    # 2. Seed some opportunities
    if db.query(Opportunity).count() == 0:
        print("Seeding opportunities...")
        opps = [
            Opportunity(
                title="Harvard Robotics Summer Internship",
                description="Join the Harvard SEAS lab for a summer of advanced robotics research. Looking for students with Python and C++ exp.",
                url="https://www.harvard.edu/robotics",
                source="Harvard",
                domain="Engineering"
            ),
            Opportunity(
                title="Yale Law Review Fellowship",
                description="Prestigious fellowship for law students interested in constitutional theory and international policy.",
                url="https://law.yale.edu/fellowship",
                source="Yale",
                domain="Law"
            ),
            Opportunity(
                title="DeepMind Scholarship 2026",
                description="Full scholarship for students pursuing PhDs in Artificial Intelligence and Neural Networks.",
                url="https://deepmind.google/scholarships",
                source="DeepMind",
                domain="Artificial Intelligence"
            ),
            Opportunity(
                title="Biomedical Innovation Hackathon",
                description="48-hour hackathon to solve modern healthcare challenges using bio-sensing tech.",
                url="https://biohack.org",
                source="Columbia",
                domain="Biomedical"
            )
        ]
        db.add_all(opps)
        db.commit()

    # 3. Seed some posts
    if db.query(Post).count() == 0:
        print("Seeding social feed...")
        demo_user = db.query(User).filter(User.email == "demo@ivy.edu").first()
        posts = [
            Post(content="Just finished my internship at DeepMind! Amazing experience working on LLMs.", author_id=demo_user.id),
            Post(content="Looking for a teammate for the upcoming Harvard Hackathon. Anyone interested in Biomedical AI?", author_id=demo_user.id),
        ]
        db.add_all(posts)
        db.commit()

    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed_db()
