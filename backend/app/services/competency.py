class InCoScoreEngine:
    # Weighted impact of different activities
    WEIGHTS = {
        "Hackathon": 50,
        "Internship": 80,
        "Research": 100,
        "Scholarship": 70,
        "Competition": 40,
        "Project": 30
    }

    @staticmethod
    def calculate_user_score(achievements):
        """
        achievements: List of achievement objects with category and title
        """
        score = 0
        for ach in achievements:
            # Get weight or default to 10 for unknown categories
            base_score = InCoScoreEngine.WEIGHTS.get(ach.category, 10)
            score += base_score
        return score

    @staticmethod
    def rank_students(db_session):
        from app.models.models import User, Profile
        return db_session.query(User).join(Profile).order_by(Profile.incoscore.desc()).all()

incoscore_engine = InCoScoreEngine()
