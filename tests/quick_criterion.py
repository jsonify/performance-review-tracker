from test_analyst_prompt import TestAnalystPrompt
import json

def main():
    test = TestAnalystPrompt()
    
    # Test entry
    entry = {
        "Title": "Performance Review System Design",
        "Description": "Created comprehensive design document for the new performance review tracking system, including detailed architecture, data models, and implementation plans.",
        "Success Notes": "Design document received positive feedback and serves as the blueprint for implementation",
        "Impact": "High"
    }
    
    print("\n=== Testing Entry ===")
    print(f"Title: {entry['Title']}")
    print(f"Description: {entry['Description']}")
    print(f"Success Notes: {entry['Success Notes']}")
    print(f"Impact: {entry['Impact']}")
    
    # Extract entry terms
    entry_text = f"{entry['Title']} {entry['Description']} {entry['Success Notes']}"
    entry_keywords = test._extract_keywords(entry_text)
    
    print("\n=== Entry Keywords ===")
    print("\nOriginal Keywords:")
    original_kw = {k for k in entry_keywords if k == test._normalize_term(k)}
    for kw in sorted(original_kw):
        print(f"- {kw}")
        
    print("\nNormalized Keywords:")
    normalized_kw = {k for k in entry_keywords if k != test._normalize_term(k)}
    for kw in sorted(normalized_kw):
        print(f"- {kw}")
    
    # Create test criterion manually
    criterion = {
        'name': 'Quality and Quantity of Work',
        'description': ' '.join([
            "Consistently produces high-quality deliverables with minimal errors",
            "Meets or exceeds deadlines",
            "Manages workload effectively",
            "Takes initiative to improve processes",
            "Demonstrates technical excellence"
        ]),
        'keywords': test._extract_keywords(
            'Quality and Quantity of Work ' +
            'Consistently produces high-quality deliverables with minimal errors ' +
            'Meets or exceeds deadlines ' +
            'Manages workload effectively ' +
            'Takes initiative to improve processes ' +
            'Demonstrates technical excellence'
        ),
        'primary_terms': {
            'quality and quantity of work': 1.0,
            'quality': 0.8,
            'quality and': 0.8,
            'quality and quantity': 0.8,
            'and quantity': 0.8,
            'and quantity of': 0.8,
            'quantity of': 0.8,
            'quantity of work': 0.8,
            'work': 0.6,
            'high-quality': 0.8,
            'technical excellence': 0.8,
            'effective': 0.7,
            'excellence': 0.7
        },
        'weight': 'High'
    }
    
    print("\n=== Criterion: Quality and Quantity of Work ===")
    print(f"\nDescription: {criterion['description']}")
    
    print("\nPrimary Terms (with weights):")
    for term, weight in sorted(criterion['primary_terms'].items(), key=lambda x: (-x[1], x[0])):
        normalized = test._normalize_term(term)
        print(f"- {term} ({normalized}): {weight:.2f}")
    
    print("\nKeywords:")
    criterion_kw = criterion['keywords']
    original_kw = {k for k in criterion_kw if k == test._normalize_term(k)}
    normalized_kw = {k for k in criterion_kw if k != test._normalize_term(k)}
    
    print("\nOriginal Keywords:")
    for kw in sorted(original_kw):
        print(f"- {kw}")
    
    print("\nNormalized Keywords:")
    for kw in sorted(normalized_kw):
        print(f"- {kw}")
    
    # Quality indicators
    print("\nQuality Indicators Found:")
    indicators = {
        'comprehensive': 0.2,
        'detailed': 0.15,
        'thorough': 0.15,
        'excellent': 0.2,
        'exceptional': 0.2,
        'high-quality': 0.2,
        'effective': 0.15,
        'efficient': 0.15,
        'reliable': 0.15,
        'consistent': 0.15,
        'complete': 0.15,
        'approved': 0.15
    }
    
    found_indicators = []
    for indicator in indicators:
        if indicator in entry_text.lower():
            found_indicators.append(f"{indicator} (+{indicators[indicator]:.2f})")
    
    if found_indicators:
        for indicator in sorted(found_indicators):
            print(f"- {indicator}")
    else:
        print("None found")
    
    # Calculate confidence
    confidence = test._calculate_match_confidence(
        entry_text.lower(),
        entry_keywords,
        criterion,
        entry['Impact']
    )
    
    print(f"\nConfidence Score: {confidence:.2f}")
    
    # Show which terms matched
    matched_keywords = criterion['keywords'] & entry_keywords
    print("\nMatched Keywords:")
    original_matches = {k for k in matched_keywords if k == test._normalize_term(k)}
    normalized_matches = {k for k in matched_keywords if k != test._normalize_term(k)}
    
    print("\nOriginal Matches:")
    for kw in sorted(original_matches):
        print(f"- {kw}")
    
    print("\nNormalized Matches:")
    for kw in sorted(normalized_matches):
        print(f"- {kw}")
    
    matched_primary = [term for term in criterion['primary_terms'] 
                      if term in entry_text.lower() or 
                      test._normalize_term(term) in entry_text.lower()]
    print("\nMatched Primary Terms:")
    for term in sorted(matched_primary):
        print(f"- {term} ({test._normalize_term(term)})")

if __name__ == '__main__':
    main()