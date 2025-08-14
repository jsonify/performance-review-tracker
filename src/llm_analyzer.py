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

def load_criteria_with_uploads(review_type: str, config: Dict = None) -> List[Dict]:
    """
    Load criteria from uploaded files first, fallback to default files.
    
    Args:
        review_type: "annual" or "competency"
        config: Configuration dict that may contain upload folder paths
        
    Returns:
        List of criteria dictionaries
    """
    # First, try to find uploaded criteria files
    upload_folders = []
    
    # Check common upload locations
    if config:
        processing_config = config.get('processing', {})
        upload_dir = processing_config.get('output_directory')
        if upload_dir:
            upload_folders.append(upload_dir)
            # Also check parent directory (ui/uploads often maps to ui/uploads)
            parent_dir = os.path.dirname(upload_dir)
            if parent_dir and parent_dir != upload_dir:
                upload_folders.append(parent_dir)
    
    # Add common upload folder locations
    upload_folders.extend([
        'ui/uploads',
        'uploads',
        'ui/results',
        'data'
    ])
    
    # Look for uploaded criteria files
    criteria_type = "annual_criteria" if review_type.lower() == "annual" else "competency_criteria"
    
    for folder in upload_folders:
        if not os.path.exists(folder):
            continue
            
        # Look for timestamped uploaded files
        try:
            files = [f for f in os.listdir(folder) 
                    if f.startswith(criteria_type) and f.endswith('.json')]
            if files:
                # Use the most recent uploaded file
                latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(folder, x)))
                criteria_path = os.path.join(folder, latest_file)
                
                print(f"DEBUG: Found uploaded criteria file: {criteria_path}")
                
                with open(criteria_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Check for standard format first: {"criteria": [...]}
                    criteria = data.get('criteria', [])
                    if criteria:
                        print(f"DEBUG: Loaded {len(criteria)} criteria from uploaded file (standard format)")
                        return criteria
                    
                    # Check for alternative format: {"Name": {"description": "...", "weight": ...}}
                    # Convert to standard format
                    if isinstance(data, dict) and not data.get('criteria'):
                        converted_criteria = []
                        for name, details in data.items():
                            if isinstance(details, dict):
                                criterion = {
                                    "name": name,
                                    "expectations": []
                                }
                                # Convert description to expectations if available
                                if 'description' in details:
                                    criterion["expectations"] = [details['description']]
                                # Add weight if available
                                if 'weight' in details:
                                    criterion["weight"] = details['weight']
                                converted_criteria.append(criterion)
                        
                        if converted_criteria:
                            print(f"DEBUG: Loaded {len(converted_criteria)} criteria from uploaded file (converted format)")
                            return converted_criteria
        except Exception as e:
            print(f"DEBUG: Error checking upload folder {folder}: {e}")
            continue
    
    # Fallback to default criteria files
    print(f"DEBUG: No uploaded criteria found, using default criteria for {review_type}")
    return load_criteria(review_type)

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
        
        # Load criteria for the review type (uploaded files first, then defaults)
        criteria = load_criteria_with_uploads(review_type, config)
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
            manual_analysis = generate_manual_analysis(data_file, review_type, criteria, config)
            with open(analysis_path, 'w', encoding='utf-8') as f:
                f.write(manual_analysis)
            print(f"DEBUG: Manual fallback analysis saved to {analysis_path}")
        
        return analysis_path
        
    except LLMClientError as e:
        logger.error(f"LLM client error: {e}")
        print(f"DEBUG: LLM client error: {e}")
        print("DEBUG: Falling back to manual analysis...")
        manual_analysis = generate_manual_analysis(data_file, review_type, criteria, config)
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(manual_analysis)
        return analysis_path
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        print(f"DEBUG: Analysis error: {e}")
        print("DEBUG: Falling back to manual analysis...")
        manual_analysis = generate_manual_analysis(data_file, review_type, criteria, config)
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(manual_analysis)
        return analysis_path

def _generate_dynamic_criteria_sections(criteria: List[Dict], data: List[Dict], accomplishment_analysis: Dict, 
                                      key_themes: List[str], technologies: List[str], business_impact: Dict,
                                      high_impact: int, total_accomplishments: int) -> str:
    """
    Generate criteria sections dynamically based on loaded criteria.
    
    Args:
        criteria: List of criteria dictionaries with name and expectations
        data: Accomplishment data
        accomplishment_analysis: Analysis results
        key_themes: Key themes extracted from accomplishments
        technologies: Technologies found in accomplishments
        business_impact: Business impact analysis
        high_impact: Number of high impact items
        total_accomplishments: Total number of accomplishments
        
    Returns:
        Formatted criteria sections as markdown string
    """
    sections = []
    
    for i, criterion in enumerate(criteria, 1):
        criterion_name = criterion.get('name', 'Unknown Criterion')
        expectations = criterion.get('expectations', [])
        
        # Generate customized content based on criterion name and expectations
        section = f"### {i}. {criterion_name}\n"
        section += "**Self Rating: 3 (Excellent)**\n\n"
        section += "**How I Met This Criterion:**\n"
        
        # Customize content based on criterion name (case-insensitive matching)
        criterion_lower = criterion_name.lower()
        
        if 'communication' in criterion_lower:
            section += f"Demonstrated excellent communication through detailed project documentation across {total_accomplishments} work items. All major projects include comprehensive acceptance criteria, technical specifications, and success verification steps, indicating superior communication of requirements and deliverables.\n"
            
        elif 'flexibility' in criterion_lower or 'agility' in criterion_lower:
            section += f"Successfully adapted across diverse technical domains spanning {', '.join(key_themes[:4])} with {len(technologies)} different technologies and platforms, demonstrating exceptional adaptability and flexibility in changing technical environments.\n"
            
        elif 'initiative' in criterion_lower or 'innovation' in criterion_lower:
            section += f"Proactively tackled complex technical challenges with {high_impact} high-impact projects demonstrating self-direction and technical leadership. Consistently identified opportunities for process improvements and technical enhancements.\n"
            
        elif 'service' in criterion_lower or 'accountability' in criterion_lower:
            section += f"Delivered comprehensive technical solutions supporting organizational infrastructure and business objectives with 100% completion rate across all {total_accomplishments} assignments, demonstrating exceptional reliability and commitment.\n"
            
        elif 'quality' in criterion_lower or 'programming' in criterion_lower or 'development' in criterion_lower:
            section += f"Achieved outstanding productivity with {total_accomplishments} completed work items while maintaining high technical standards. Quality demonstrated through {accomplishment_analysis['detailed_count']} projects with comprehensive documentation and {accomplishment_analysis['avg_description_length']:.0f} average characters of technical detail per project.\n"
            
        elif 'teamwork' in criterion_lower or 'inclusion' in criterion_lower or 'influence' in criterion_lower:
            section += f"Collaborated effectively on complex technical projects supporting team goals through knowledge sharing and technical leadership. Contributed to inclusive practices and positive team dynamics across all project engagements.\n"
            
        elif 'architecture' in criterion_lower or 'design' in criterion_lower:
            section += f"Designed and implemented scalable technical solutions across {len(key_themes)} major technical domains, demonstrating strong architectural thinking and system design capabilities with focus on long-term maintainability.\n"
            
        elif 'problem' in criterion_lower or 'testing' in criterion_lower:
            section += f"Systematically identified and resolved complex technical issues with comprehensive problem-solving approach. All projects include detailed acceptance criteria and verification procedures ensuring robust problem resolution.\n"
            
        elif 'project' in criterion_lower or 'management' in criterion_lower:
            section += f"Successfully managed technical project execution from requirements through delivery across {total_accomplishments} work items, demonstrating strong project coordination and delivery management capabilities.\n"
            
        else:
            # Generic content for unrecognized criteria
            section += f"Successfully demonstrated this competency through {total_accomplishments} completed work items, showing consistent performance and professional excellence in this area. Expertise evidenced through detailed project documentation and successful delivery outcomes.\n"
        
        # Add expectations if available
        if expectations:
            section += f"\n**Key Expectations Met:**\n"
            for expectation in expectations[:3]:  # Limit to top 3 expectations
                section += f"- {expectation}\n"
        
        section += "\n"
        sections.append(section)
    
    return '\n'.join(sections)

def generate_manual_analysis(data_file: str, review_type: str, criteria: List[Dict] = None, config: Dict = None) -> str:
    """
    Generate intelligent manual analysis when LLM analysis fails.
    Uses keyword analysis and content extraction to provide meaningful insights.
    
    Args:
        data_file: Path to processed JSON data
        review_type: Type of review
        criteria: Optional list of criteria dictionaries to use instead of defaults
        config: Optional configuration dict for finding uploaded criteria
        
    Returns:
        Manual analysis content as markdown string
    """
    # Load criteria if not provided
    if criteria is None:
        criteria = load_criteria_with_uploads(review_type, config)
        print(f"DEBUG: generate_manual_analysis loaded {len(criteria)} criteria")
    
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

{_generate_dynamic_criteria_sections(criteria, data, accomplishment_analysis, key_themes, technologies, business_impact, high_impact, total_accomplishments)}

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

Based on {total_accomplishments} completed work items, this assessment evaluates performance across {len(criteria)} professional competency areas:

{_generate_dynamic_criteria_sections(criteria, data, accomplishment_analysis, key_themes, technologies, business_impact, high_impact, total_accomplishments)}

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
                found_technologies.extend([f"Version {v}" for v in list(set(versions))[:5]])
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
    elif provider not in ["requestyai", "openai", "anthropic", "google", "azure_openai", "ollama", "roo_code"]:
        issues.append(f"Unsupported LLM provider: {provider}")
    
    # Check provider-specific requirements
    if provider in ["requestyai", "openai", "anthropic", "google"]:
        if not llm_config.get("api_key"):
            issues.append(f"API key required for {provider}")
    
    if provider == "azure_openai":
        if not llm_config.get("api_key"):
            issues.append("API key required for Azure OpenAI")
        if not llm_config.get("options", {}).get("azure_endpoint"):
            issues.append("Azure endpoint required for Azure OpenAI")
    
    # Check model specification
    model = llm_config.get("model", "")
    if not model and provider not in ["roo_code"]:
        issues.append(f"Model not specified for {provider}")
    
    return issues