#!/usr/bin/env python3
"""
LLM Analysis Module for Performance Review System

This module replaces the Roo Code integration with direct LLM API calls.
It provides analysis of work accomplishments against performance criteria
using various LLM providers.
"""

import json
import os
import logging
from typing import Dict, List, Optional
try:
    from .llm_client import create_llm_client, LLMClientError
except ImportError:
    from llm_client import create_llm_client, LLMClientError

logger = logging.getLogger(__name__)

def load_criteria(review_type: str) -> List[Dict]:
    """
    Load criteria from JSON files based on review type.
    
    Args:
        review_type: "annual" or "competency"
        
    Returns:
        List of criteria dictionaries
    """
    if review_type.lower() == "annual":
        criteria_file = "criteria/annual_review_criteria.json"
    else:
        criteria_file = "criteria/competency_assessment_criteria.json"
    
    if not os.path.exists(criteria_file):
        raise FileNotFoundError(f"Criteria file not found: {criteria_file}")
    
    with open(criteria_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('criteria', [])

def run_llm_analysis(data_file: str, review_type: str, config: Dict) -> str:
    """
    Run LLM analysis on the processed data, replacing run_roo_code_analysis.
    
    Args:
        data_file: Path to processed JSON data file
        review_type: Type of review ("annual" or "competency")
        config: Application configuration dictionary
        
    Returns:
        Path to analysis file
    """
    print(f"DEBUG: run_llm_analysis - START {data_file} {review_type}")
    print(f"DEBUG: Config provider: {config.get('llm_integration', {}).get('provider', 'None')}")
    
    # Determine output path for the analysis
    analysis_path = data_file.replace('processed_', 'analyzed_').replace('.json', '.md')
    
    try:
        # Load the processed accomplishments
        with open(data_file, 'r', encoding='utf-8') as f:
            accomplishments = json.load(f)
        
        if not accomplishments:
            logger.warning("No accomplishments found in processed data")
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write("No accomplishments found in the processed data.")
            return analysis_path
        
        print(f"DEBUG: Loaded {len(accomplishments)} accomplishments for analysis")
        print(f"DEBUG: Sample accomplishment titles: {[acc.get('Title', 'N/A')[:50] for acc in accomplishments[:3]]}")
        
        # Load criteria for the review type
        criteria = load_criteria(review_type)
        print(f"DEBUG: Loaded {len(criteria)} criteria for {review_type} review")
        print(f"DEBUG: Sample criteria: {[c.get('name', 'N/A') for c in criteria[:5]]}")
        
        # Try to create LLM client
        try:
            llm_client = create_llm_client(config)
            print(f"DEBUG: Created LLM client with provider: {llm_client.provider.value}")
            
            # Test connection
            print("DEBUG: Testing LLM connection...")
            if not llm_client.test_connection():
                print("DEBUG: LLM connection test failed - falling back to enhanced manual analysis")
                raise LLMClientError("LLM provider connection failed")
                
        except ImportError as e:
            print(f"DEBUG: LLM library not available ({e}) - using enhanced manual analysis")
            raise LLMClientError(f"Required library not available: {e}")
        except Exception as e:
            print(f"DEBUG: LLM client creation failed ({e}) - using enhanced manual analysis")
            raise LLMClientError(f"Client initialization failed: {e}")
        
        print(f"DEBUG: Successfully connected to {llm_client.provider.value} provider")
        
        # Run the analysis
        response = llm_client.analyze_accomplishments(
            accomplishments=accomplishments,
            criteria=criteria,
            review_type=review_type
        )
        
        if response.success:
            # Save the analysis to file
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write(response.content)
            
            print(f"DEBUG: Analysis completed successfully using {response.provider}")
            print(f"DEBUG: Analysis saved to: {analysis_path}")
            
            # Log performance metrics
            if response.processing_time:
                print(f"DEBUG: Processing time: {response.processing_time:.2f} seconds")
            if response.tokens_used:
                print(f"DEBUG: Tokens used: {response.tokens_used}")
        else:
            # Analysis failed, try manual fallback
            logger.error(f"LLM analysis failed: {response.error_message}")
            print("DEBUG: LLM analysis failed, generating manual fallback...")
            manual_analysis = generate_manual_analysis(data_file, review_type)
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write(manual_analysis)
            print(f"DEBUG: Manual fallback analysis saved to {analysis_path}")
        
        return analysis_path
        
    except LLMClientError as e:
        logger.error(f"LLM client error: {e}")
        print(f"DEBUG: LLM client error: {e}")
        print("DEBUG: Falling back to manual analysis...")
        manual_analysis = generate_manual_analysis(data_file, review_type)
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(manual_analysis)
        return analysis_path
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        print(f"DEBUG: Analysis error: {e}")
        print("DEBUG: Falling back to manual analysis...")
        manual_analysis = generate_manual_analysis(data_file, review_type)
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(manual_analysis)
        return analysis_path

def generate_manual_analysis(data_file: str, review_type: str) -> str:
    """
    Generate intelligent manual analysis when LLM analysis fails.
    Uses keyword analysis and content extraction to provide meaningful insights.
    
    Args:
        data_file: Path to processed JSON data
        review_type: Type of review
        
    Returns:
        Manual analysis content as markdown string
    """
    # Load the processed data
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    total_accomplishments = len(data)
    if total_accomplishments == 0:
        return "No accomplishments found in the processed data."
    
    # Import competency mapping for better analysis
    try:
        from .competency_keywords import COMPETENCY_KEYWORDS, map_accomplishments_to_competencies
    except ImportError:
        from competency_keywords import COMPETENCY_KEYWORDS, map_accomplishments_to_competencies
    
    # Analyze impact distribution
    high_impact = len([item for item in data if item.get('Impact') == 'High'])
    medium_impact = len([item for item in data if item.get('Impact') == 'Medium'])
    low_impact = len([item for item in data if item.get('Impact') == 'Low'])
    
    # Extract date range
    dates = [item['Date'] for item in data if 'Date' in item]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "Date range not available"
    
    # Perform intelligent content analysis
    accomplishment_analysis = _analyze_accomplishment_content(data)
    
    # Map accomplishments to competencies for better insights
    competency_mapping = map_accomplishments_to_competencies(data, min_score=0.1)
    
    # Extract key themes and technologies
    key_themes = _extract_key_themes(data)
    technologies = _extract_technologies(data)
    business_impact = _analyze_business_impact(data)
    
    if review_type.lower() == 'annual':
        # Generate intelligent analysis using extracted insights
        top_accomplishments = accomplishment_analysis['top_detailed']
        tech_summary = ', '.join(technologies[:8]) if technologies else 'Various technical systems'
        theme_summary = ', '.join(key_themes[:5]) if key_themes else 'Multi-domain technical work'
        
        return f"""# Annual Review Analysis

## Executive Summary
Successfully completed **{total_accomplishments} work items** during the review period ({date_range}), demonstrating expertise in {theme_summary.lower()} and technical proficiency across {len(technologies)} technologies including {tech_summary}.

**Impact Distribution:**
- High Impact: {high_impact} items ({high_impact/total_accomplishments*100:.1f}%)
- Medium Impact: {medium_impact} items ({medium_impact/total_accomplishments*100:.1f}%)
- Low Impact: {low_impact} items ({low_impact/total_accomplishments*100:.1f}%)

**Technical Scope:**
- **Primary Focus Areas:** {', '.join(key_themes[:3]) if key_themes else 'Infrastructure, Development, Integration'}
- **Technologies Used:** {', '.join(technologies[:10]) if technologies else 'Various enterprise technologies'}
- **Detailed Projects:** {accomplishment_analysis['detailed_count']} work items with comprehensive technical documentation
- **Average Project Complexity:** {accomplishment_analysis['avg_description_length']:.0f} characters of technical detail per project

## Criterion Analysis

### 1. Communication
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Demonstrated exceptional technical communication through detailed project documentation. Notable examples include:

{_format_specific_accomplishments(top_accomplishments[:2], 'communication')}

All {accomplishment_analysis['detailed_count']} complex projects include comprehensive acceptance criteria, technical specifications, and success verification steps, indicating superior communication of technical requirements and deliverables.

### 2. Flexibility
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Successfully adapted across diverse technical domains spanning {', '.join(key_themes[:4])}. Worked with {len(technologies)} different technologies and platforms, demonstrating exceptional adaptability:

{_format_specific_accomplishments(top_accomplishments[:2], 'flexibility')}

### 3. Initiative
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Proactively tackled complex technical challenges with {high_impact} high-impact projects demonstrating self-direction and technical leadership. Examples of initiative include:

{_format_specific_accomplishments([acc for acc in top_accomplishments if 'high' in acc.get('title', '').lower()][:2], 'initiative')}

### 4. Member Service
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Delivered comprehensive technical solutions supporting organizational infrastructure and business objectives. Service excellence demonstrated through:

{_format_business_impact_examples(business_impact, data)}

### 5. Personal Credibility
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Demonstrated exceptional reliability with 100% completion rate across all {total_accomplishments} technical assignments. Credibility established through:

- Comprehensive technical documentation for all major projects
- {accomplishment_analysis['detailed_count']} projects with detailed acceptance criteria and verification steps
- Consistent delivery of complex technical solutions requiring specialized expertise

### 6. Quality and Quantity of Work
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Achieved outstanding productivity with {total_accomplishments} completed work items while maintaining high technical standards. Quality indicators:

- {accomplishment_analysis['detailed_count']} projects with comprehensive technical documentation
- Average of {accomplishment_analysis['avg_description_length']:.0f} characters of technical detail per project
- {high_impact} high-impact technical deliverables providing significant organizational value
- Expertise demonstrated across {len(key_themes)} major technical domains

### 7. Teamwork
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Collaborated effectively on complex technical projects supporting team goals through knowledge sharing and technical leadership. Examples include:

{_format_specific_accomplishments(top_accomplishments[:2], 'teamwork')}

## Overall Summary

Delivered exceptional technical performance with {total_accomplishments} successfully completed work items spanning {date_range}. Demonstrated advanced technical competencies across multiple domains with particular expertise in {', '.join(key_themes[:3])}.

**Key Technical Accomplishments:**
- **{accomplishment_analysis['detailed_count']} Complex Projects:** Average {accomplishment_analysis['avg_description_length']:.0f} characters of technical documentation per project
- **{len(technologies)} Technologies:** Including {', '.join(technologies[:5])} and others
- **{high_impact} High-Impact Deliverables:** Providing significant organizational and technical value
- **Multi-Domain Expertise:** Spanning {', '.join(key_themes[:5])}

**Areas of Technical Excellence:**
- Comprehensive technical documentation and requirements analysis
- Multi-platform and multi-technology expertise
- Complex system installation, configuration, and integration
- Proactive problem-solving and technical leadership

**Business Impact Categories:**
{_format_business_impact_summary(business_impact)}

_Intelligent analysis generated from {total_accomplishments} completed work items with {accomplishment_analysis['detailed_count']} detailed technical projects during {date_range}_
"""

    else:  # competency review
        return f"""# Competency Assessment Analysis

## Executive Summary
Successfully completed **{total_accomplishments} work items** during the assessment period ({date_range}), demonstrating technical competency and professional development across multiple technical domains.

**Impact Distribution:**
- High Impact: {high_impact} items
- Medium Impact: {medium_impact} items  
- Low Impact: {low_impact} items

## Competency Analysis

Based on {total_accomplishments} completed work items, this assessment evaluates performance across 13 professional competency areas:

### Programming/Software Development
**Rating: 3 (Practicing)**
Demonstrated consistent application of programming and development skills across multiple work items with independent execution and quality deliverables.

### Solution Architecture  
**Rating: 2 (Developing)**
Applied architectural thinking to technical solutions with growing proficiency in system design and integration approaches.

### Systems Design
**Rating: 2 (Developing)**
Contributed to system design initiatives with increasing understanding of scalability and integration requirements.

### Project Management
**Rating: 3 (Practicing)**
Successfully managed {total_accomplishments} work items from initiation through completion, demonstrating effective project execution skills.

### Requirements Definition
**Rating: 3 (Practicing)**
Consistently delivered work items meeting defined acceptance criteria, showing strong requirements analysis and implementation capabilities.

### Testing
**Rating: 2 (Developing)**
Applied testing practices and validation approaches with growing proficiency in quality assurance methodologies.

### Problem Management
**Rating: 3 (Practicing)**
Effectively resolved technical challenges across {total_accomplishments} work items, demonstrating systematic problem-solving abilities.

### Innovation
**Rating: 2 (Developing)**
Contributed creative solutions and process improvements with increasing confidence in innovative approaches.

### Release/Deployment
**Rating: 2 (Developing)**
Participated in deployment activities with growing understanding of release management and production considerations.

### Accountability
**Rating: 4 (Mastering)**
Demonstrated exceptional accountability with 100% completion rate across all assigned work items and consistent follow-through on commitments.

### Influence
**Rating: 2 (Developing)**
Building influence through reliable delivery and technical contributions, with opportunities for expanded leadership impact.

### Agility
**Rating: 3 (Practicing)**
Successfully adapted to changing requirements and priorities across diverse work items, maintaining effectiveness during transitions.

### Inclusion
**Rating: 2 (Developing)**
Contributed to team success through collaborative execution and knowledge sharing opportunities.

## Overall Assessment

Strong competency development demonstrated through {total_accomplishments} successfully completed work items. Particular strength in accountability, project execution, and technical problem-solving. Opportunities for continued growth in leadership influence and architectural design capabilities.

**Development Recommendations:**
- Continue building solution architecture experience through complex system design projects
- Expand leadership influence through mentoring and cross-team collaboration
- Deepen innovation capabilities through process improvement initiatives

_Assessment based on {total_accomplishments} work items completed during {date_range}_
"""


def _analyze_accomplishment_content(data: List[Dict]) -> Dict[str, any]:
    """
    Analyze the actual content of accomplishments for meaningful insights.
    
    Args:
        data: List of accomplishment dictionaries
        
    Returns:
        Dictionary with content analysis insights
    """
    import re
    from collections import Counter
    
    # Extract all text content for analysis
    all_text = ""
    detailed_accomplishments = []
    
    for item in data:
        title = item.get('Title', '')
        description = item.get('Description', '')
        criteria = item.get('Acceptance Criteria', '')
        notes = item.get('Success Notes', '')
        
        # Combine all text
        combined_text = f"{title} {description} {criteria} {notes}".lower()
        all_text += " " + combined_text
        
        # Track accomplishments with substantial detail
        if len(description) > 50 or len(criteria) > 50:
            detailed_accomplishments.append({
                'title': title,
                'description': description[:200] + "..." if len(description) > 200 else description,
                'complexity_score': len(description) + len(criteria)
            })
    
    # Extract version numbers, technologies, and technical terms
    version_pattern = r'\b\d+\.\d+(?:\.\d+)?\b'
    versions = re.findall(version_pattern, all_text)
    
    # Common technical terms to look for
    tech_terms = ['api', 'database', 'server', 'application', 'system', 'security', 'deployment', 
                  'configuration', 'integration', 'performance', 'architecture', 'infrastructure',
                  'testing', 'monitoring', 'automation', 'migration', 'upgrade', 'installation']
    
    found_tech_terms = [term for term in tech_terms if term in all_text]
    
    return {
        'detailed_count': len(detailed_accomplishments),
        'top_detailed': detailed_accomplishments[:5],  # Top 5 most detailed
        'versions_mentioned': list(set(versions))[:10],  # Unique versions
        'technical_terms': found_tech_terms,
        'avg_description_length': sum(len(item.get('Description', '')) for item in data) / len(data) if data else 0
    }


def _extract_key_themes(data: List[Dict]) -> List[str]:
    """
    Extract key themes from accomplishment titles and descriptions.
    
    Args:
        data: List of accomplishment dictionaries
        
    Returns:
        List of key themes identified
    """
    from collections import Counter
    import re
    
    # Common project/work themes
    theme_keywords = {
        'Infrastructure': ['server', 'infrastructure', 'network', 'deployment', 'installation', 'configuration'],
        'Security': ['security', 'authentication', 'authorization', 'compliance', 'vulnerability'],
        'Development': ['development', 'coding', 'programming', 'application', 'software', 'code'],
        'Database': ['database', 'sql', 'data', 'migration', 'backup', 'storage'],
        'Integration': ['integration', 'api', 'service', 'connector', 'interface'],
        'Automation': ['automation', 'script', 'automated', 'batch', 'scheduled'],
        'Testing': ['testing', 'test', 'qa', 'quality', 'validation', 'verification'],
        'Monitoring': ['monitoring', 'logging', 'metrics', 'alerting', 'dashboard'],
        'Training': ['training', 'learning', 'education', 'course', 'certification'],
        'Support': ['support', 'troubleshooting', 'maintenance', 'fix', 'resolution']
    }
    
    # Combine all text content
    all_text = " ".join([
        f"{item.get('Title', '')} {item.get('Description', '')}".lower()
        for item in data
    ])
    
    # Count theme occurrences
    theme_scores = {}
    for theme, keywords in theme_keywords.items():
        score = sum(all_text.count(keyword) for keyword in keywords)
        if score > 0:
            theme_scores[theme] = score
    
    # Return top themes sorted by relevance
    return sorted(theme_scores.keys(), key=theme_scores.get, reverse=True)


def _extract_technologies(data: List[Dict]) -> List[str]:
    """
    Extract specific technologies and tools mentioned in accomplishments.
    
    Args:
        data: List of accomplishment dictionaries
        
    Returns:
        List of technologies identified
    """
    import re
    
    # Technology patterns to look for
    tech_patterns = {
        'Operating Systems': ['rhel', 'red hat', 'linux', 'windows', 'ubuntu', 'centos'],
        'Databases': ['mysql', 'postgresql', 'oracle', 'mongodb', 'sql server', 'sqlite'],
        'Cloud Platforms': ['aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes'],
        'Programming Languages': ['python', 'java', 'javascript', 'c#', 'ruby', 'php', 'go'],
        'Tools & Frameworks': ['artifactory', 'jenkins', 'git', 'apache', 'nginx', 'elasticsearch'],
        'Versions': r'\b\d+\.\d+(?:\.\d+)?\b'  # Version numbers
    }
    
    # Combine all text
    all_text = " ".join([
        f"{item.get('Title', '')} {item.get('Description', '')} {item.get('Acceptance Criteria', '')}".lower()
        for item in data
    ])
    
    found_technologies = []
    
    # Search for technology mentions
    for category, patterns in tech_patterns.items():
        if category == 'Versions':
            versions = re.findall(patterns, all_text)
            if versions:
                found_technologies.extend([f"Version {v}" for v in set(versions)[:5]])
        else:
            for pattern in patterns:
                if pattern in all_text:
                    found_technologies.append(pattern.title())
    
    return list(set(found_technologies))[:15]  # Limit to 15 unique technologies


def _analyze_business_impact(data: List[Dict]) -> Dict[str, any]:
    """
    Analyze business impact indicators in accomplishments.
    
    Args:
        data: List of accomplishment dictionaries
        
    Returns:
        Dictionary with business impact analysis
    """
    impact_keywords = {
        'Efficiency': ['efficiency', 'optimize', 'improve', 'streamline', 'faster', 'performance'],
        'Cost Savings': ['cost', 'save', 'reduce', 'budget', 'resource', 'efficient'],
        'Quality': ['quality', 'reliability', 'stability', 'availability', 'uptime'],
        'Security': ['security', 'compliance', 'audit', 'vulnerability', 'risk'],
        'User Experience': ['user', 'customer', 'experience', 'interface', 'usability'],
        'Scalability': ['scale', 'capacity', 'growth', 'expansion', 'volume']
    }
    
    all_text = " ".join([
        f"{item.get('Description', '')} {item.get('Success Notes', '')}".lower()
        for item in data
    ])
    
    impact_scores = {}
    for category, keywords in impact_keywords.items():
        score = sum(all_text.count(keyword) for keyword in keywords)
        if score > 0:
            impact_scores[category] = score
    
    # Find accomplishments with quantifiable results
    quantifiable = []
    for item in data:
        text = f"{item.get('Description', '')} {item.get('Success Notes', '')}".lower()
        # Look for numbers, percentages, time savings, etc.
        if any(indicator in text for indicator in ['%', 'percent', 'hour', 'day', 'faster', 'reduced', 'increased']):
            quantifiable.append(item.get('Title', 'Unnamed accomplishment'))
    
    return {
        'impact_categories': sorted(impact_scores.keys(), key=impact_scores.get, reverse=True),
        'quantifiable_results': quantifiable[:5],
        'total_impact_mentions': sum(impact_scores.values())
    }


def _format_specific_accomplishments(accomplishments: List[Dict], context: str) -> str:
    """
    Format specific accomplishments for criterion examples.
    
    Args:
        accomplishments: List of accomplishment dictionaries
        context: The criterion context (communication, flexibility, etc.)
        
    Returns:
        Formatted string with specific examples
    """
    if not accomplishments:
        return "- Consistently delivered high-quality technical solutions across all assigned projects"
    
    formatted_examples = []
    for i, acc in enumerate(accomplishments[:3], 1):  # Limit to top 3
        title = acc.get('title', 'Technical Project')
        description = acc.get('description', 'No description available')[:150]
        if len(acc.get('description', '')) > 150:
            description += "..."
        
        formatted_examples.append(f"- **{title}:** {description}")
    
    return '\n'.join(formatted_examples)


def _format_business_impact_examples(business_impact: Dict, data: List[Dict]) -> str:
    """
    Format business impact examples with specific accomplishments.
    
    Args:
        business_impact: Business impact analysis results
        data: Full accomplishments data
        
    Returns:
        Formatted string with business impact examples
    """
    if not business_impact.get('impact_categories'):
        return "- Delivered technical solutions supporting critical organizational infrastructure and business operations"
    
    examples = []
    top_categories = business_impact['impact_categories'][:3]
    
    for category in top_categories:
        examples.append(f"- **{category}:** Demonstrated through multiple technical implementations and system improvements")
    
    if business_impact.get('quantifiable_results'):
        examples.append(f"- **Measurable Results:** Including projects with quantifiable outcomes such as {', '.join(business_impact['quantifiable_results'][:3])}")
    
    return '\n'.join(examples)


def _format_business_impact_summary(business_impact: Dict) -> str:
    """
    Format business impact summary for the overall review.
    
    Args:
        business_impact: Business impact analysis results
        
    Returns:
        Formatted summary string
    """
    if not business_impact.get('impact_categories'):
        return "- Multiple areas of organizational impact through technical excellence and reliable delivery"
    
    categories = business_impact['impact_categories'][:4]
    return '\n'.join([f"- **{category}:** Technical contributions supporting organizational objectives" for category in categories])

def validate_llm_config(config: Dict) -> List[str]:
    """
    Validate LLM configuration and return any issues found.
    
    Args:
        config: Application configuration dictionary
        
    Returns:
        List of validation issues (empty if valid)
    """
    issues = []
    
    llm_config = config.get("llm_integration", {})
    
    if not llm_config:
        issues.append("No llm_integration section found in configuration")
        return issues
    
    provider = llm_config.get("provider", "").lower()
    if not provider:
        issues.append("LLM provider not specified")
    elif provider not in ["openai", "anthropic", "google", "azure_openai", "ollama", "roo_code"]:
        issues.append(f"Unsupported LLM provider: {provider}")
    
    # Check provider-specific requirements
    if provider in ["openai", "anthropic", "google"]:
        if not llm_config.get("api_key"):
            issues.append(f"API key required for {provider}")
    
    if provider == "azure_openai":
        if not llm_config.get("api_key"):
            issues.append("API key required for Azure OpenAI")
        if not llm_config.get("options", {}).get("azure_endpoint"):
            issues.append("Azure endpoint required for Azure OpenAI")
    
    # Check model specification
    model = llm_config.get("model", "")
    if not model and provider != "roo_code":
        issues.append(f"Model not specified for {provider}")
    
    return issues