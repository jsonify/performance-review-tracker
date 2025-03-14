"""
Tests for competency keyword mapping functionality.
"""

import pytest
from src.competency_keywords import (
    COMPETENCY_KEYWORDS,
    get_competency_score,
    map_accomplishment,
    map_accomplishments_to_competencies
)

@pytest.fixture
def sample_accomplishments():
    return [
        {
            "Title": "Python ETL Pipeline Development",
            "Description": "Developed a Python-based ETL pipeline for processing data",
            "Success Notes": "Improved efficiency by 85%, automated daily processing"
        },
        {
            "Title": "System Architecture Design",
            "Description": "Designed scalable microservices architecture",
            "Success Notes": "Successfully implemented distributed system"
        },
        {
            "Title": "Team Mentoring Initiative",
            "Description": "Led technical mentoring program for junior developers",
            "Success Notes": "Improved team productivity and knowledge sharing"
        }
    ]

def test_competency_keywords_structure():
    """Test that all competencies have reasonable keyword lists."""
    for competency, keywords in COMPETENCY_KEYWORDS.items():
        assert len(keywords) >= 5, f"{competency} should have at least 5 keywords"
        assert all(isinstance(k, str) for k in keywords), f"{competency} has non-string keywords"
        assert all(k.strip() == k for k in keywords), f"{competency} has keywords with whitespace"

def test_get_competency_score():
    """Test competency relevance scoring."""
    text = "Developed a Python application with automated tests"
    
    # Should have high score for programming
    prog_score = get_competency_score(text, COMPETENCY_KEYWORDS["Programming/Software Development"])
    assert prog_score > 0.2
    
    # Should have low score for inclusion
    incl_score = get_competency_score(text, COMPETENCY_KEYWORDS["Inclusion"])
    assert incl_score < 0.2

def test_get_competency_score_case_insensitive():
    """Test that scoring is case insensitive."""
    text = "PYTHON development and Testing"
    lower_text = text.lower()
    
    score1 = get_competency_score(text, COMPETENCY_KEYWORDS["Programming/Software Development"])
    score2 = get_competency_score(lower_text, COMPETENCY_KEYWORDS["Programming/Software Development"])
    
    assert score1 == score2

def test_map_accomplishment():
    """Test mapping single accomplishment text to competencies."""
    text = "Developed a Python ETL pipeline with automated testing"
    
    matches = map_accomplishment(text)
    
    # Should match programming and testing
    assert "Programming/Software Development" in matches
    assert "Testing" in matches
    
    # Should not match inclusion
    assert "Inclusion" not in matches

def test_map_accomplishment_threshold():
    """Test minimum score threshold for mapping."""
    text = "Some generic text with no strong competency signals"
    
    # With low threshold
    matches_low = map_accomplishment(text, min_score=0.01)
    
    # With high threshold
    matches_high = map_accomplishment(text, min_score=0.5)
    
    assert len(matches_low) > len(matches_high)

def test_map_accomplishments_to_competencies(sample_accomplishments):
    """Test mapping multiple accomplishments to competencies."""
    result = map_accomplishments_to_competencies(sample_accomplishments)
    
    # Check programming competency
    prog_matches = result["Programming/Software Development"]
    assert any("Python ETL" in acc["Title"] for acc in prog_matches)
    
    # Check architecture competency
    arch_matches = result["Solution Architecture"]
    assert any("System Architecture" in acc["Title"] for acc in arch_matches)
    
    # Check inclusion/influence competency
    influence_matches = result["Influence"]
    assert any("Team Mentoring" in acc["Title"] for acc in influence_matches)

def test_map_accomplishments_to_competencies_empty():
    """Test mapping with empty accomplishments list."""
    result = map_accomplishments_to_competencies([])
    
    assert isinstance(result, dict)
    assert all(isinstance(v, list) for v in result.values())
    assert all(len(v) == 0 for v in result.values())

def test_map_accomplishments_multiple_competencies(sample_accomplishments):
    """Test that accomplishments can map to multiple competencies."""
    result = map_accomplishments_to_competencies(sample_accomplishments, min_score=0.1)
    
    # Count how many competencies each accomplishment maps to
    acc_competency_counts = {}
    for comp, accs in result.items():
        for acc in accs:
            title = acc["Title"]
            acc_competency_counts[title] = acc_competency_counts.get(title, 0) + 1
    
    # Check that at least one accomplishment maps to multiple competencies
    assert any(count > 1 for count in acc_competency_counts.values())

def test_keyword_uniqueness():
    """Test that important keywords are not overused across competencies."""
    # Get all keywords for each competency
    all_keywords = {}
    for comp, keywords in COMPETENCY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in all_keywords:
                all_keywords[keyword].append(comp)
            else:
                all_keywords[keyword] = [comp]
    
    # Check for keywords that appear in too many competencies
    overused = {k: v for k, v in all_keywords.items() if len(v) > 3}
    
    # Some overlap is OK, but shouldn't be too much
    assert len(overused) < len(all_keywords) * 0.1, \
        f"Too many overused keywords: {overused}"

def test_competency_distinctiveness():
    """Test that competencies have sufficiently distinct keywords."""
    for comp1, keywords1 in COMPETENCY_KEYWORDS.items():
        for comp2, keywords2 in COMPETENCY_KEYWORDS.items():
            if comp1 >= comp2:
                continue
            
            # Calculate overlap
            overlap = set(keywords1) & set(keywords2)
            total = set(keywords1) | set(keywords2)
            
            # Overlap should be less than 30% of total keywords
            overlap_ratio = len(overlap) / len(total)
            assert overlap_ratio < 0.3, \
                f"Too much overlap between {comp1} and {comp2}: {overlap}"