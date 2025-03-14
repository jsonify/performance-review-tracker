"""
Example of using the CompetencyFormatter with keyword-based accomplishment mapping.
"""

import csv
import json
from typing import Dict, List
from pathlib import Path
from competency_formatter import CompetencyFormatter
from competency_keywords import map_accomplishments_to_competencies, COMPETENCY_KEYWORDS

def load_accomplishments(filepath: str) -> List[Dict]:
    """Load accomplishments from CSV file."""
    accomplishments = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            accomplishments.append(row)
    return accomplishments

def load_competency_definitions(filepath: str) -> Dict:
    """Load competency rating definitions."""
    with open(filepath, 'r') as f:
        return {row['Topic']: row for row in csv.DictReader(f)}

def get_rating_definition(definitions: Dict, competency: str, rating: int) -> str:
    """Get the definition for a specific competency rating level."""
    comp_def = definitions.get(competency, {})
    rating_key = f"{rating} - " + {
        1: "Learning",
        2: "Developing",
        3: "Practicing",
        4: "Mastering",
        5: "Leading"
    }[rating]
    return comp_def.get(rating_key, "")

def analyze_impact_trends(accomplishments: List[Dict]) -> Dict[str, Dict]:
    """
    Analyze impact trends over time for each competency.
    Returns a dict of competency -> impact statistics
    """
    competency_impacts = {}
    
    # Use keyword mapping to associate accomplishments with competencies
    comp_map = map_accomplishments_to_competencies(accomplishments)
    
    for competency, accs in comp_map.items():
        if not accs:
            continue
            
        # Count impact levels
        impact_counts = {
            "High": len([a for a in accs if a['Impact'] == 'High']),
            "Medium": len([a for a in accs if a['Impact'] == 'Medium']),
            "Low": len([a for a in accs if a['Impact'] == 'Low'])
        }
        
        # Calculate trends
        recent_accs = [a for a in accs if '2025' in a['Date']]
        recent_high_impact = len([a for a in recent_accs if a['Impact'] == 'High'])
        
        competency_impacts[competency] = {
            "total_accomplishments": len(accs),
            "impact_counts": impact_counts,
            "recent_accomplishments": len(recent_accs),
            "recent_high_impact": recent_high_impact,
            "avg_impact": (impact_counts["High"] * 3 + impact_counts["Medium"] * 2 + impact_counts["Low"]) / len(accs)
        }
    
    return competency_impacts

def generate_assessment_data(
    accomplishments: List[Dict],
    definitions: Dict,
    competency: str,
    impact_analysis: Dict
) -> Dict:
    """Generate assessment data for a single competency."""
    # Get mapped accomplishments
    comp_map = map_accomplishments_to_competencies(accomplishments)
    comp_accomplishments = comp_map.get(competency, [])
    
    if not comp_accomplishments:
        return None

    # Calculate rating based on impact analysis
    impact_stats = impact_analysis[competency]
    
    # Rating calculation factors:
    # - Average impact of accomplishments
    # - Recent high-impact achievements
    # - Total number of accomplishments
    base_rating = min(5, round(impact_stats["avg_impact"] * 1.5))
    
    if impact_stats["recent_high_impact"] > 0:
        base_rating = min(5, base_rating + 1)
    
    if impact_stats["total_accomplishments"] < 2:
        base_rating = min(base_rating, 3)
    
    rating = max(1, min(5, base_rating))

    # Get top 3 accomplishments by impact
    evidence = []
    for impact in ['High', 'Medium', 'Low']:
        impact_accs = [acc for acc in comp_accomplishments if acc['Impact'] == impact]
        for acc in sorted(impact_accs, key=lambda x: x['Date'], reverse=True):
            evidence_text = f"{acc['Title']}: {acc['Success Notes']}"
            if acc['Impact'] == 'High':
                evidence_text += " [High Impact]"
            evidence.append(evidence_text)
            if len(evidence) >= 3:
                break
        if len(evidence) >= 3:
            break

    # Get key achievements
    achievements = [
        acc['Title']
        for acc in sorted(comp_accomplishments, 
                         key=lambda x: (x['Impact'] == 'High', x['Date']), 
                         reverse=True)[:3]
    ]

    # Generate impact analysis
    impact = (
        f"This competency is demonstrated through {impact_stats['total_accomplishments']} significant "
        f"accomplishments, including {impact_stats['impact_counts']['High']} high-impact and "
        f"{impact_stats['impact_counts']['Medium']} medium-impact achievements. "
    )
    
    if impact_stats['recent_high_impact'] > 0:
        impact += (
            f"Notable recent activity includes {impact_stats['recent_high_impact']} high-impact "
            f"achievements in the current year, showing continued growth and expertise. "
        )
    
    impact += (
        f"These contributions have demonstrated consistent ability to deliver valuable results "
        f"and drive improvements in this competency area."
    )

    # Generate growth narrative if relevant
    growth = None
    if impact_stats['recent_high_impact'] > 0 and rating >= 4:
        growth = (
            f"Recent high-impact achievements demonstrate growing mastery of this competency. "
            f"Consistent delivery of significant results and leadership in complex initiatives "
            f"shows strong potential for continued growth and increased responsibility. "
            f"Pattern of success suggests readiness for more strategic roles."
        )

    return {
        "name": competency,
        "rating": rating,
        "evidence": evidence,
        "rating_definition": get_rating_definition(definitions, competency, rating),
        "achievements": achievements,
        "impact": impact,
        "growth": growth
    }

def main():
    # Initialize formatter
    formatter = CompetencyFormatter()
    
    # Load data
    data_dir = Path('data')
    accomplishments = load_accomplishments(data_dir / 'accomplishments.csv')
    definitions = load_competency_definitions(data_dir / 'competencies-formatted.csv')
    
    # Analyze impact trends
    impact_analysis = analyze_impact_trends(accomplishments)
    
    # Generate competency assessments
    competencies = []
    
    for competency in COMPETENCY_KEYWORDS.keys():
        if competency in impact_analysis:
            assessment = generate_assessment_data(
                accomplishments=accomplishments,
                definitions=definitions,
                competency=competency,
                impact_analysis=impact_analysis
            )
            if assessment:
                competencies.append(assessment)
    
    # Sort competencies by rating (highest first)
    competencies.sort(key=lambda x: x['rating'], reverse=True)
    
    # Generate summary
    high_rated = [c for c in competencies if c['rating'] >= 4]
    avg_rating = sum(c['rating'] for c in competencies) / len(competencies)
    
    summary = (
        f"Overall performance demonstrates strong technical capabilities with an average "
        f"competency rating of {avg_rating:.1f}/5. "
    )
    
    if high_rated:
        summary += (
            f"Particularly strong performance in: "
            f"{', '.join(c['name'] for c in high_rated)}. "
        )
    
    total_high_impact = sum(
        impact_analysis[c['name']]['impact_counts']['High']
        for c in competencies
    )
    
    summary += (
        f"Delivered {total_high_impact} high-impact achievements across "
        f"{len(competencies)} competency areas, showing consistent ability to "
        f"drive significant improvements and technical excellence."
    )
    
    # Generate and save report
    report = formatter.generate_report(
        summary=summary,
        competencies=competencies
    )
    
    # Ensure output directory exists
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    # Save report
    with open(output_dir / 'competency_assessment.md', 'w') as f:
        f.write(report)
    
    print(f"Generated assessment with {len(competencies)} competencies")
    print(f"Average rating: {avg_rating:.1f}")
    print(f"Report saved to: {output_dir / 'competency_assessment.md'}")

if __name__ == '__main__':
    main()