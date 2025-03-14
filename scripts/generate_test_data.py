#!/usr/bin/env python3
"""
Generates sample accomplishment data for testing the competency assessment system.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Sample data components
PROJECTS = [
    "API Development",
    "Database Migration",
    "CI/CD Pipeline",
    "Cloud Infrastructure",
    "Security Framework",
    "Testing Automation",
    "Performance Optimization",
    "Data Processing",
    "System Integration",
    "Monitoring Solution"
]

ACTIONS = [
    "Developed",
    "Implemented",
    "Designed",
    "Created",
    "Optimized",
    "Enhanced",
    "Architected",
    "Deployed",
    "Streamlined",
    "Automated"
]

TECHNOLOGIES = [
    "Python",
    "JavaScript",
    "Docker",
    "Kubernetes",
    "AWS",
    "Jenkins",
    "PostgreSQL",
    "React",
    "GraphQL",
    "Terraform"
]

IMPACTS = ["High", "Medium", "Low"]
IMPACT_WEIGHTS = [0.3, 0.5, 0.2]  # 30% High, 50% Medium, 20% Low

def generate_title():
    """Generate a random project title."""
    return f"{random.choice(ACTIONS)} {random.choice(PROJECTS)} using {random.choice(TECHNOLOGIES)}"

def generate_description(title):
    """Generate a detailed description based on the title."""
    background = random.choice([
        "Legacy system needed modernization",
        "Manual process was inefficient",
        "Scaling issues required architectural changes",
        "Security vulnerabilities needed addressing",
        "Performance bottlenecks impacted users"
    ])
    
    return f"{title}.\n\nBackground: {background}."

def generate_success_notes():
    """Generate success metrics."""
    improvements = [
        "Reduced processing time by {}%",
        "Improved efficiency by {}%",
        "Increased throughput by {}%",
        "Reduced error rate by {}%",
        "Decreased response time by {}%"
    ]
    
    metrics = [
        "Achieved {}% test coverage",
        "Handled {} requests per second",
        "Saved {} hours per week",
        "Reduced costs by {}%",
        "Improved user satisfaction by {}%"
    ]
    
    notes = []
    
    # Add 2-3 improvements
    for _ in range(random.randint(2, 3)):
        improvement = random.choice(improvements)
        percentage = random.randint(20, 95)
        notes.append(improvement.format(percentage))
        
    # Add 1-2 metrics
    for _ in range(random.randint(1, 2)):
        metric = random.choice(metrics)
        value = random.randint(20, 95)
        notes.append(metric.format(value))
        
    return "\n".join(notes)

def generate_date(start_date, end_date):
    """Generate a random date between start and end dates."""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

def generate_accomplishments(num_entries=10, output_file="data/accomplishments.csv"):
    """Generate sample accomplishment data."""
    # Ensure output directory exists
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate accomplishments
    accomplishments = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for _ in range(num_entries):
        title = generate_title()
        date = generate_date(start_date, end_date)
        
        accomplishment = {
            "Timestamp": date.strftime("%m/%d/%Y %H:%M:%S"),
            "Date": date.strftime("%m/%d/%Y"),
            "Title": title,
            "Description": generate_description(title),
            "Success Notes": generate_success_notes(),
            "Impact": random.choices(IMPACTS, weights=IMPACT_WEIGHTS)[0]
        }
        accomplishments.append(accomplishment)
    
    # Sort by date
    accomplishments.sort(key=lambda x: datetime.strptime(x["Date"], "%m/%d/%Y"), reverse=True)
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=accomplishments[0].keys())
        writer.writeheader()
        writer.writerows(accomplishments)
    
    print(f"Generated {num_entries} sample accomplishments in {output_file}")
    print("\nAccomplishment distribution:")
    impact_counts = {impact: len([a for a in accomplishments if a["Impact"] == impact]) 
                    for impact in IMPACTS}
    for impact, count in impact_counts.items():
        print(f"- {impact}: {count} ({count/num_entries*100:.1f}%)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate sample accomplishment data")
    parser.add_argument("--num", type=int, default=10, help="Number of accomplishments to generate")
    parser.add_argument("--output", default="data/accomplishments.csv", help="Output file path")
    args = parser.parse_args()
    
    generate_accomplishments(args.num, args.output)