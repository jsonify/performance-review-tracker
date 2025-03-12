from test_analyst_prompt import TestAnalystPrompt

def main():
    test = TestAnalystPrompt()
    
    # Test entry text
    text = "Created comprehensive design document for the new performance review tracking system, including detailed architecture, data models, and implementation plans."
    
    print("\n=== Testing Term Normalization ===")
    test_terms = [
        'quality',
        'qualities',
        'qualitative',
        'document',
        'documentation',
        'documenting',
        'design',
        'designing',
        'designed',
        'performance',
        'performing',
        'comprehensive',
        'comprehensively'
    ]
    
    print("\nNormalized Forms:")
    for term in test_terms:
        norm = test._normalize_term(term)
        print(f"{term:15} -> {norm}")
    
    print("\n=== Testing Quality Boost Calculation ===")
    criterion_names = [
        "Quality and Quantity of Work",
        "Technical Excellence",
        "System Design",
        "Documentation Standards"
    ]
    
    print("\nQuality Boosts by Criterion:")
    for name in criterion_names:
        boost = test._calculate_quality_boost(text, name)
        print(f"{name:25} -> {boost:.2f}")
    
    print("\n=== Keywords in Test Text ===")
    keywords = test._extract_keywords(text)
    print("\nOriginal Keywords:")
    original = {k for k in keywords if k == test._normalize_term(k)}
    for k in sorted(original):
        print(f"- {k}")
        
    print("\nNormalized Keywords:")
    normalized = {k for k in keywords if k != test._normalize_term(k)}
    for k in sorted(normalized):
        print(f"- {k}")
    
    print("\n=== Testing Primary Term Matching ===")
    primary_terms = {
        'quality and quantity of work': 1.0,
        'technical excellence': 0.8,
        'comprehensive documentation': 0.8,
        'design document': 0.8,
        'system design': 0.8,
        'architecture': 0.7,
        'implementation': 0.7
    }
    
    print("\nMatched Primary Terms:")
    for term, weight in primary_terms.items():
        if term in text.lower() or test._normalize_term(term) in text.lower():
            print(f"- {term} (weight: {weight:.1f})")

if __name__ == '__main__':
    main()