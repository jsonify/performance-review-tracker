"""
Keyword mappings for mapping accomplishments to competencies.
These help identify which accomplishments demonstrate each competency.
"""

COMPETENCY_KEYWORDS = {
    "Programming/Software Development": [
        "code", "develop", "programming", "python", "javascript", "java",
        "software", "implementation", "coding", "engineer", "script",
        "module", "library", "api", "algorithm", "debug", "refactor"
    ],
    
    "Solution Architecture": [
        "architect", "design", "structure", "system", "infrastructure",
        "platform", "framework", "scalability", "integration", "microservice",
        "distributed", "cloud", "aws", "azure", "solution", "component"
    ],
    
    "Systems Design": [
        "design pattern", "component", "interface", "schema", "model",
        "workflow", "process flow", "system integration", "data model",
        "architecture", "specification", "technical design", "blueprint"
    ],
    
    "Project Management": [
        "project", "timeline", "milestone", "deadline", "budget",
        "stakeholder", "resource", "planning", "coordination", "schedule",
        "risk", "scope", "deliverable", "manage", "track"
    ],
    
    "Requirements Definition": [
        "requirement", "specification", "scope", "user story", "user need",
        "business need", "functional", "non-functional", "acceptance criteria",
        "validation", "verification", "stakeholder", "define"
    ],
    
    "Testing": [
        "test", "quality", "qa", "verification", "validation",
        "unit test", "integration test", "automation", "coverage",
        "regression", "assert", "mock", "stub", "test case", "test plan"
    ],
    
    "Problem Management": [
        "problem", "issue", "incident", "resolution", "root cause",
        "troubleshoot", "debug", "fix", "solve", "diagnose",
        "investigate", "analysis", "monitoring", "alert"
    ],
    
    "Innovation": [
        "innovation", "improve", "enhance", "optimize", "automate",
        "efficiency", "novel", "creative", "solution", "initiative",
        "modernize", "transform", "streamline", "pioneering"
    ],
    
    "Release and Deployment": [
        "release", "deploy", "delivery", "pipeline", "ci/cd",
        "configuration", "version", "build", "package", "install",
        "upgrade", "rollout", "migration", "continuous integration"
    ],
    
    "Accountability": [
        "responsible", "ownership", "lead", "drive", "deliver",
        "manage", "oversee", "coordinate", "ensure", "maintain",
        "commitment", "reliable", "dependable", "track"
    ],
    
    "Influence": [
        "influence", "lead", "guide", "mentor", "teach",
        "present", "communicate", "collaborate", "coordinate",
        "facilitate", "advocate", "recommend", "convince"
    ],
    
    "Agility": [
        "adapt", "flexible", "change", "learn", "improve",
        "responsive", "adjust", "evolve", "pivot", "dynamic",
        "resilient", "versatile", "quick", "efficient"
    ],
    
    "Inclusion": [
        "team", "collaborate", "inclusive", "diverse", "mentor",
        "support", "help", "teach", "share", "guide",
        "contribute", "participate", "involve", "engage"
    ]
}

def get_competency_score(text: str, keywords: list) -> float:
    """
    Calculate a relevance score for how well a text matches competency keywords.
    
    Args:
        text: The text to analyze
        keywords: List of keywords to look for
        
    Returns:
        Float between 0-1 indicating relevance
    """
    text = text.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text)
    return matches / len(keywords)

def map_accomplishment(text: str, min_score: float = 0.1) -> list:
    """
    Map an accomplishment to relevant competencies based on keyword matching.
    
    Args:
        text: The accomplishment text to analyze
        min_score: Minimum relevance score to consider (0-1)
        
    Returns:
        List of competencies that match above the minimum score
    """
    matches = []
    for competency, keywords in COMPETENCY_KEYWORDS.items():
        score = get_competency_score(text, keywords)
        if score >= min_score:
            matches.append((competency, score))
    
    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches]

# Example accomplishment mapper function that uses keyword matching
def map_accomplishments_to_competencies(accomplishments, min_score=0.1):
    """
    Group accomplishments by competency using keyword analysis.
    
    Args:
        accomplishments: List of accomplishment dictionaries
        min_score: Minimum relevance score to consider (0-1)
        
    Returns:
        Dict mapping competencies to lists of relevant accomplishments
    """
    competency_map = {comp: [] for comp in COMPETENCY_KEYWORDS.keys()}
    
    for acc in accomplishments:
        # Combine relevant text fields for analysis
        text = f"{acc['Title']} {acc['Description']} {acc['Success Notes']}"
        
        # Find matching competencies
        matches = map_accomplishment(text, min_score)
        
        # Add to each matching competency's list
        for competency in matches:
            competency_map[competency].append(acc)
            
    return competency_map