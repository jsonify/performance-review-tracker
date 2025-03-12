from test_analyst_prompt import TestAnalystPrompt
import json

def main():
    # Create test instance
    test = TestAnalystPrompt()
    
    print("\n=== Loading Test Data ===")
    # Load sample data
    with open('data/sample_accomplishments.json', 'r') as f:
        sample_data = json.load(f)
    print(f"Loaded {len(sample_data)} sample entries")
    
    print("\n=== Loading System Prompt ===")
    # Load system prompt
    with open('.roo/system-prompt-analyst', 'r') as f:
        system_prompt = f.read()
    print("System prompt loaded")
    
    print("\n=== Extracting Annual Review Criteria ===")
    annual_criteria = test._extract_detailed_criteria(system_prompt, 'ANNUAL REVIEWS')
    print(f"\nFound {len(annual_criteria)} annual review criteria:")
    for c in annual_criteria:
        print(f"\n{c['name']} (Weight: {c['weight']})")
        print("Keywords:", ', '.join(sorted(c['keywords'])[:10]))
    
    print("\n=== Extracting Competency Assessment Criteria ===")
    competency_criteria = test._extract_detailed_criteria(system_prompt, 'COMPETENCY ASSESSMENTS')
    print(f"\nFound {len(competency_criteria)} competency assessment criteria:")
    for c in competency_criteria:
        print(f"\n{c['name']} (Weight: {c['weight']})")
        print("Keywords:", ', '.join(sorted(c['keywords'])[:10]))
    
    print("\n=== Testing First Entry ===")
    entry = sample_data[0]
    print(f"\nAnalyzing: {entry['Title']}")
    print(f"Description: {entry['Description']}")
    print(f"Impact: {entry['Impact']}")
    
    # Extract entry keywords
    entry_text = f"{entry['Title']} {entry['Description']} {entry['Success Notes']}"
    entry_keywords = test._extract_keywords(entry_text)
    print("\nEntry Keywords:", ', '.join(sorted(entry_keywords)[:10]))
    
    # Find matches
    matches = test._find_criteria_matches(entry, annual_criteria, competency_criteria)
    if matches:
        print("\nMatched Criteria:")
        for match in matches:
            print(f"\n- {match['criterion']}: {match['confidence']:.2f}")
            print("  Matched Keywords:", ', '.join(sorted(match['keywords_matched'])[:10]))
    else:
        print("\nNo criteria matches found!")

if __name__ == '__main__':
    main()