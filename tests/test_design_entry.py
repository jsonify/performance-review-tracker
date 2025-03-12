import json

def main():
    # test = TestAnalystPrompt()
    
    print("\n=== Testing Performance Review System Design Entry ===")
    
    # Load test entry
    test_entry = {
        "Date": "2024-10-15",
        "Title": "Performance Review System Design",
        "Description": "Created comprehensive design document for the new performance review tracking system, including detailed architecture, data models, and implementation plans.",
        "Acceptance Criteria": "Complete technical specification approved by stakeholders",
        "Success Notes": "Design document received positive feedback and serves as the blueprint for implementation",
        "Impact": "High"
    }
    
    # Load system prompt
    with open('.roo/system-prompt-analyst', 'r') as f:
        system_prompt = f.read()
    
    # Get criteria
    # annual_criteria = test._extract_detailed_criteria(system_prompt, 'ANNUAL REVIEWS')
    # competency_criteria = test._extract_detailed_criteria(system_prompt, 'COMPETENCY ASSESSMENTS')
    
    print("\nEntry Details:")
    print(f"Title: {test_entry['Title']}")
    print(f"Description: {test_entry['Description']}")
    print(f"Success Notes: {test_entry['Success Notes']}")
    print(f"Impact: {test_entry['Impact']}")
    
    # Extract entry keywords
    # entry_text = f"{test_entry['Title']} {test_entry['Description']} {test_entry['Success Notes']}"
    # entry_keywords = test._extract_keywords(entry_text)
    # print(f"\nExtracted Keywords ({len(entry_keywords)}):")
    # print(', '.join(sorted(entry_keywords)))
    
    # Test against specific criteria that should match
    # expected_matches = [
    #     'Quality and Quantity of Work',
    #     'Systems Design',
    #     'Solution Architecture',
    #     'Project Management',
    #     'Technical'
    # ]
    
    # print("\nTesting against expected matching criteria:")
    # for criterion_name in expected_matches:
    #     print(f"\nLooking for matches with: {criterion_name}")
        
    #     # Find the criterion in our lists
    #     criterion = None
    #     # for c in annual_criteria + competency_criteria:
    #     #     if criterion_name.lower() in c['name'].lower():
    #     #         criterion = c
    #     #         break
        
    #     if criterion:
    #         print(f"Found criterion: {criterion['name']} (Weight: {criterion['weight']})")
    #         print(f"Primary terms: {', '.join(criterion['primary_terms'])}")
    #         print(f"Keywords: {', '.join(sorted(criterion['keywords'])[:10])}")
            
    #         # Calculate confidence
    #         # confidence = test._calculate_match_confidence(
    #         #     entry_text.lower(),
    #         #     entry_keywords,
    #         #     criterion,
    #         #     test_entry['Impact']
    #         # )
    #         print(f"Match confidence: {confidence:.2f}")
            
    #         # Show matching keywords
    #         # matched_keywords = criterion['keywords'] & entry_keywords
    #         print(f"Matched keywords: {', '.join(sorted(matched_keywords))}")
            
    #         # Show if we have strong evidence
    #         # has_strong = test._has_strong_evidence(entry_text.lower(), criterion['name'])
    #         print(f"Has strong evidence: {has_strong}")
    #     else:
    #         print(f"ERROR: Criterion {criterion_name} not found in criteria lists!")
    
    # Get all matches
    print("\nAll criteria matches: Skipped")
    # matches = test._find_criteria_matches(test_entry, annual_criteria, competency_criteria)
    
    # if matches:
    #     for match in matches:
    #         print(f"\n- {match['criterion']}: {match['confidence']:.2f}")
    #         print(f"  Matched Keywords: {', '.join(sorted(match['keywords_matched']))}")
    # else:
    #     print("\nNo criteria matches found!")

if __name__ == '__main__':
    main()