import shutil
import os
from fastapi import UploadFile
from typing import Dict
import PyPDF2
import re

UPLOAD_DIR = "uploads"

class AutoAppService:
    @staticmethod
    def save_resume(user_id: int, file: UploadFile) -> str:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        
        file_path = os.path.join(UPLOAD_DIR, f"user_{user_id}_resume.pdf")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    @staticmethod
    def extract_info_from_pdf(file_path: str) -> Dict[str, str]:
        """
        Extracts contact info and skills from a PDF resume.
        """
        extracted_text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted_text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PDF Extraction Error: {e}")
            return {"error": "Failed to parse PDF"}

        # Basic RegEx for data extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', extracted_text)
        email = email_match.group(0) if email_match else "Extracted Email"
        
        # Look for skills (simulated keyword matching)
        common_skills = ["Python", "Java", "SQL", "Machine Learning", "React", "Law", "Biology", "Finance"]
        found_skills = [skill for skill in common_skills if skill.lower() in extracted_text.lower()]
        
        return {
            "email": email,
            "skills": ", ".join(found_skills) if found_skills else "General Research",
            "education": "Ivy League Candidate" if "college" in extracted_text.lower() or "university" in extracted_text.lower() else "Student",
            "experience_snippet": extracted_text[:200].replace('\n', ' ') + "..."
        }

    @staticmethod
    def autofill_form(user_profile, opportunity):
        return {
            "full_name": user_profile.user.full_name,
            "email": user_profile.user.email,
            "interest_statement": f"I am deeply motivated by {opportunity.title} because it bridges my interest in {user_profile.interests} with real-world impact.",
            "relevant_skills": user_profile.skills or "Advanced Research & Analytical Writing",
            "resume_link": f"/api/profile/resume/{user_profile.user_id}"
        }

auto_app_service = AutoAppService()
