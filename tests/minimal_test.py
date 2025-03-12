from test_analyst_prompt import TestAnalystPrompt

def print_section(prompt, start_marker):
    """Print the section of text starting with the given marker"""
    lines = prompt.split('\n')
    start_idx = -1
    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
            break
    
    if start_idx >= 0:
        print(f"\nFound section starting with '{start_marker}' at line {start_idx + 1}:")
        for i in range(start_idx, min(start_idx + 10, len(lines))):
            print(f"{i+1:3d} | {lines[i]}")
    else:
        print(f"\nSection '{start_marker}' not found!")

def main():
    # Create test instance
    test = TestAnalystPrompt()
    
    # Load system prompt
    print("Loading system prompt...")
    with open('.roo/system-prompt-analyst', 'r') as f:
        prompt = f.read()
    
    # Print relevant sections
    print_section(prompt, "For ANNUAL REVIEWS")
    print_section(prompt, "For COMPETENCY ASSESSMENTS")
    
    # Extract criteria
    print("\nExtracting annual review criteria...")
    annual = test._extract_detailed_criteria(prompt, "ANNUAL REVIEWS")
    print(f"\nFound {len(annual)} annual review criteria:")
    for c in annual:
        print(f"\n- {c['name']} (Weight: {c['weight']})")
    
    print("\nExtracting competency assessment criteria...")
    comp = test._extract_detailed_criteria(prompt, "COMPETENCY ASSESSMENTS")
    print(f"\nFound {len(comp)} competency assessment criteria:")
    for c in comp:
        print(f"\n- {c['name']} (Weight: {c['weight']})")

if __name__ == '__main__':
    main()