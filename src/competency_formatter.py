"""
Formats competency assessments into properly structured Markdown documents.
Ensures consistent formatting and comprehensive justification sections.
"""

from typing import List, Dict, Optional

class CompetencyFormatter:
    def __init__(self):
        self.template = """# Competency Assessment Report

## Summary
{summary}

{competencies}
"""

        self.competency_template = """## {name}

### Rating: {rating}/5

### Evidence
{evidence}

### Justification
{justification}

---
"""

    def format_evidence(self, evidence_list: List[str]) -> str:
        """
        Formats evidence items as a Markdown list with proper indentation.
        
        Args:
            evidence_list: List of evidence statements
            
        Returns:
            Formatted Markdown bullet points
        """
        if not evidence_list:
            return "*No evidence provided*"
            
        return "\n".join(f"- {evidence}" for evidence in evidence_list)

    def format_justification(self, 
                           rating: int,
                           rating_definition: str,
                           achievements: List[str],
                           impact: str,
                           growth: Optional[str] = None) -> str:
        """
        Creates a comprehensive justification section with multiple paragraphs.
        
        Args:
            rating: Numerical rating 1-5
            rating_definition: The formal definition for this rating level
            achievements: List of key achievements demonstrating the rating
            impact: Description of business impact
            growth: Optional growth trajectory
            
        Returns:
            Multi-paragraph justification text
        """
        paragraphs = []
        
        # Rating context paragraph
        paragraphs.append(f"Based on the demonstrated achievements, a rating of {rating}/5 " 
                         f"({rating_definition}) is warranted.")
        
        # Achievements paragraph
        achievement_text = " ".join(f"* {achievement}" for achievement in achievements)
        paragraphs.append(f"The following key accomplishments support this rating: {achievement_text}")
        
        # Impact paragraph
        paragraphs.append(impact)
        
        # Optional growth trajectory
        if growth:
            paragraphs.append(growth)
            
        return "\n\n".join(paragraphs)

    def format_competency(self,
                         name: str,
                         rating: int,
                         evidence: List[str],
                         rating_definition: str,
                         achievements: List[str],
                         impact: str,
                         growth: Optional[str] = None) -> str:
        """
        Formats a complete competency section.
        
        Args:
            name: Competency name
            rating: Numerical rating 1-5
            evidence: List of evidence points
            rating_definition: Definition of the assigned rating level
            achievements: Key achievements supporting the rating
            impact: Business impact description
            growth: Optional growth trajectory
            
        Returns:
            Formatted Markdown for the competency section
        """
        return self.competency_template.format(
            name=name,
            rating=rating,
            evidence=self.format_evidence(evidence),
            justification=self.format_justification(
                rating=rating,
                rating_definition=rating_definition,
                achievements=achievements,
                impact=impact,
                growth=growth
            )
        )

    def generate_report(self,
                       summary: str,
                       competencies: List[Dict]) -> str:
        """
        Generates a complete competency assessment report.
        
        Args:
            summary: Overall performance summary
            competencies: List of competency dictionaries containing:
                - name: str
                - rating: int
                - evidence: List[str]
                - rating_definition: str
                - achievements: List[str]
                - impact: str
                - growth: Optional[str]
                
        Returns:
            Complete Markdown document as string
        """
        formatted_competencies = []
        for comp in competencies:
            formatted_competencies.append(self.format_competency(**comp))
            
        return self.template.format(
            summary=summary,
            competencies="\n".join(formatted_competencies)
        )

# Example usage:
if __name__ == "__main__":
    formatter = CompetencyFormatter()
    
    # Example competency data
    example = {
        "name": "Programming/Software Development",
        "rating": 4,
        "evidence": [
            "Developed Jenkins pipeline reducing deployment time from 2 hours to 15 minutes",
            "Created Python ETL pipeline improving processing efficiency by 85%",
            "Implemented automated testing framework achieving 95% coverage"
        ],
        "rating_definition": "Takes technical responsibility across all stages and iterations of software development",
        "achievements": [
            "Automated critical deployment processes",
            "Significantly improved data processing efficiency",
            "Enhanced quality through test automation"
        ],
        "impact": ("These improvements have had substantial business impact, reducing operational costs "
                  "while improving reliability and scalability. The automated systems now handle "
                  "critical business processes with minimal manual intervention, allowing the team "
                  "to focus on strategic initiatives."),
        "growth": ("Demonstrated progression from individual contributor to technical leader, "
                  "regularly sharing knowledge and mentoring team members on best practices.")
    }
    
    # Generate example report
    report = formatter.generate_report(
        summary="Demonstrated strong technical leadership and innovation across multiple projects.",
        competencies=[example]
    )
    
    # Example of saving to file
    with open("output/competency_assessment.md", "w") as f:
        f.write(report)