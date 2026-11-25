import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.config import get_settings
from app.services.semantic_matcher import semantic_similarity

SKILL_VOCABULARY = {"python", "java", "javascript", "typescript", "react", "fastapi", "sql", "postgresql", "docker", "aws", "azure", "git", "kubernetes", "pandas", "scikit-learn", "machine learning", "rest api", "api", "agile", "scrum"}


@dataclass
class MatchResult:
    score: float
    skills_score: float
    experience_score: float
    education_score: float
    keywords_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]
    explanation: str


def _skills(text: str) -> set[str]:
    normalized = text.lower()
    return {skill for skill in SKILL_VOCABULARY if re.search(r"(?<![a-z])" + re.escape(skill) + r"(?![a-z])", normalized)}


def analyze(cv_text: str, job_text: str) -> MatchResult:
    cv_skills, job_skills = _skills(cv_text), _skills(job_text)
    matched = sorted(cv_skills & job_skills)
    missing = sorted(job_skills - cv_skills)
    skills_score = len(matched) / len(job_skills) if job_skills else 0.0
    cv_lower, job_lower = cv_text.lower(), job_text.lower()
    experience_score = 1.0 if re.search(r"\b\d+\+?\s+years?\b", cv_lower) and re.search(r"\b\d+\+?\s+years?\b", job_lower) else 0.0
    education_terms = ("bachelor", "master", "degree", "phd", "university")
    education_score = 1.0 if any(term in cv_lower for term in education_terms) and any(term in job_lower for term in education_terms) else 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        keywords_score = float(cosine_similarity(vectorizer.fit_transform([cv_text, job_text]))[0, 1])
    except ValueError:
        keywords_score = 0.0
    semantic_note = ""
    if get_settings().enable_semantic_matching:
        semantic_score = semantic_similarity(cv_text, job_text)
        if semantic_score is not None:
            keywords_score = (keywords_score + max(0.0, semantic_score)) / 2
            semantic_note = " Optional semantic similarity was blended with TF-IDF."
    score = round((skills_score * .50 + experience_score * .25 + education_score * .15 + keywords_score * .10) * 100, 2)
    recommendations = [f"Add evidence for: {', '.join(missing)}." for _ in [0] if missing]
    if not experience_score:
        recommendations.append("Clarify years of relevant experience with measurable outcomes.")
    if not education_score:
        recommendations.append("Include relevant education or certifications when applicable.")
    explanation = f"Matched {len(matched)} of {len(job_skills)} detected skills. The score uses skills 50%, experience 25%, education 15%, and TF-IDF keywords 10%; missing evidence is scored as zero.{semantic_note}"
    return MatchResult(score, skills_score, experience_score, education_score, keywords_score, matched, missing, recommendations, explanation)

