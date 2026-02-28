from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import re

class IvyIntelligence:
    def __init__(self):
        self.domains = ["Artificial Intelligence", "Law", "Biomedical", "Engineering", "Arts", "Business", "Research", "Public Policy"]
        # Expanded training corpus for better classification
        self.training_corpus = [
            ("Deep learning, neural networks, computer vision, robotics, AI, machine learning, NLP, transformers", "Artificial Intelligence"),
            ("Constitution, civil rights, litigation, legal scholarship, courts, justice, law school, juris doctor", "Law"),
            ("Molecular biology, genetics, medical devices, neuroengineering, pharmaceuticals, clinical trials, healthcare", "Biomedical"),
            ("Mechanical systems, civil engineering, aerospace, thermodynamics, structural design, bridge, electrical", "Engineering"),
            ("Art history, classical music, digital humanities, literature, museum, theater, fine arts", "Arts"),
            ("Venture capital, entrepreneurship, finance, management, startup, marketing, sales, accounting", "Business"),
            ("Academic research, lab assistant, citation, peer review, data analysis, methodology, thesis", "Research"),
            ("Government, international relations, policy analysis, advocacy, diplomacy, political science", "Public Policy")
        ]
        self._build_classifier()

    def _build_classifier(self):
        texts, labels = zip(*self.training_corpus)
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 2))
        X = self.vectorizer.fit_transform(texts)
        self.classifier = MultinomialNB()
        self.classifier.fit(X, labels)

    def classify(self, text):
        if not text: return "General"
        X = self.vectorizer.transform([text])
        return self.classifier.predict(X)[0]

    def calculate_match_score(self, profile_interests: str, opp_desc: str) -> float:
        """
        Computes a realistic match score using TF-IDF similarity and keyword boosting.
        """
        if not profile_interests or not opp_desc:
            return 0.0
        
        # Clean text
        profile_interests = profile_interests.lower()
        opp_desc = opp_desc.lower()
        print(f"[AI_MATCH] Profile: {profile_interests[:50]}... | Opp: {opp_desc[:50]}...")
        
        try:
            # Local vectorizer for the specific comparison
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform([profile_interests, opp_desc])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Base score from similarity
            score = similarity * 100
            
            # Strategic Keyword Boosting
            interests_list = [i.strip() for i in re.split(',| ', profile_interests) if len(i.strip()) > 2]
            bonus = 0
            for interest in interests_list:
                if interest in opp_desc:
                    bonus += 15 # Increased boost for direct keyword hits
            
            final_score = min(round(score + bonus, 2), 100.0)
            print(f"[AI_MATCH] Final Score: {final_score}")
            return final_score
        except Exception as e:
            print(f"[AI_MATCH] ERROR: {e}")
            return 0.0

intelligence_engine = IvyIntelligence()
