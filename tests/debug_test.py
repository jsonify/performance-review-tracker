from test_analyst_prompt import TestAnalystPrompt
import json
import os
import sys
import traceback

def check_files_exist():
    """Verify required files exist"""
    required_files = [
        'data/sample_accomplishments.json',
        'data/test_accomplishments.json',
        '.roo/system-prompt-analyst'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"ERROR: Required file not found: {file_path}")
            return False
    return True

def load_test_data():
    """Load test data directly"""
    all_data = []
    
    try:
        # Load original sample data
        with open('data/sample_accomplishments.json', 'r') as f:
            all_data.extend(json.load(f))
        
        # Load additional test data
        with open('data/test_accomplishments.json', 'r') as f:
            all_data.extend(json.load(f))
            
        return all_data
    except Exception as e:
        print(f"ERROR loading test data: {str(e)}")
        return None

def load_system_prompt():
    """Load system prompt directly"""
    try:
        with open('.roo/system-prompt-analyst', 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR loading system prompt: {str(e)}")
        return None

def main():
    print("\n=== Performance Review Analysis Debug Test ===\n")
    
    # Check required files
    if not check_files_exist():
        sys.exit(1)
    
    # Create test instance
    test = TestAnalystPrompt()
    
    # Load data
    print("Loading test data...")
    sample_data = load_test_data()
    if not sample_data:
        sys.exit(1)
    print(f"Loaded {len(sample_data)} test entries")
    
    print("\nLoading system prompt...")
    system_prompt = load_system_prompt()
    if not system_prompt:
        sys.exit(1)
    print("System prompt loaded successfully")
    
    print("\n=== Testing Data Structure ===")
    try:
        if test.verify_data_structure(sample_data):
            print("✓ Data structure test passed")
    except Exception as e:
        print(f"✗ Data structure test failed: {str(e)}")
        print(traceback.format_exc())
        sys.exit(1)
    
    print("\n=== Testing Criteria Coverage ===")
    try:
        # Extract criteria
        print("\nExtracting criteria definitions...")
        annual_criteria = test._extract_detailed_criteria(system_prompt, 'ANNUAL REVIEWS')
        competency_criteria = test._extract_detailed_criteria(system_prompt, 'COMPETENCY ASSESSMENTS')
        
        print("\nExtracted Criteria:")
        print("\nAnnual Review Criteria:")
        for c in annual_criteria:
            print(f"\n{c['name']} (Weight: {c['weight']}):")
            print(f"Keywords: {', '.join(sorted(c['keywords'])[:20])}") # Show first 20 keywords only
            if len(c['keywords']) > 20:
                print(f"...and {len(c['keywords']) - 20} more keywords")
        
        print("\nCompetency Assessment Criteria:")
        for c in competency_criteria:
            print(f"\n{c['name']} (Weight: {c['weight']}):")
            print(f"Keywords: {', '.join(sorted(c['keywords'])[:20])}") # Show first 20 keywords only
            if len(c['keywords']) > 20:
                print(f"...and {len(c['keywords']) - 20} more keywords")
        
        print("\nAnalyzing Accomplishments:")
        for entry in sample_data:
            print(f"\n{'=' * 80}")
            print(f"Entry: {entry['Title']}")
            print(f"Description: {entry['Description']}")
            print(f"Impact: {entry['Impact']}")
            
            # Extract entry keywords
            entry_text = f"{entry['Title']} {entry['Description']} {entry['Success Notes']}"
            entry_keywords = test._extract_keywords(entry_text)
            print(f"\nExtracted Keywords ({len(entry_keywords)} total):")
            print(', '.join(sorted(entry_keywords)[:20]))
            if len(entry_keywords) > 20:
                print(f"...and {len(entry_keywords) - 20} more keywords")
            
            # Find matches
            matches = test._find_criteria_matches(entry, annual_criteria, competency_criteria)
            if matches:
                print("\nMatched Criteria (sorted by confidence):")
                for match in matches:
                    print(f"\n- {match['criterion']}: {match['confidence']:.2f}")
                    print(f"  Matched Keywords ({len(match['keywords_matched'])} total):")
                    print(f"  {', '.join(sorted(match['keywords_matched'])[:10])}")
                    if len(match['keywords_matched']) > 10:
                        print(f"  ...and {len(match['keywords_matched']) - 10} more matches")
            else:
                print("\n*** No criteria matches found! ***")
            print('=' * 80)
        
        # Try the full coverage test
        print("\nRunning full criteria coverage test...")
        test.test_criteria_coverage(sample_data, system_prompt)
        print("✓ Criteria coverage test passed")
    except Exception as e:
        print(f"\n✗ Criteria coverage test failed: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        sys.exit(1)
    
    print("\n=== Test Suite Complete ===")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())
        sys.exit(1)