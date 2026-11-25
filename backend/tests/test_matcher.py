from app.services.matcher import analyze


def test_matcher_is_deterministic_and_explainable() -> None:
    result = analyze("Python SQL Docker and 5 years experience, bachelor degree", "Python SQL Docker 3 years experience bachelor degree")
    assert result.score > 50
    assert result.matched_skills == ["docker", "python", "sql"]
    assert result.missing_skills == []
    assert "skills 50%" in result.explanation

