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
        
        # Load criteria for the review type
        criteria = load_criteria(review_type)
        print(f"DEBUG: Loaded {len(criteria)} criteria for {review_type} review")
        
        # Create LLM client
        llm_client = create_llm_client(config)
        
        # Test connection if this is the first run
        if not llm_client.test_connection():
            raise LLMClientError("LLM provider connection failed")
        
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
    Generate manual analysis when LLM analysis fails.
    This is the same fallback function from main.py but moved here for better organization.
    
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
    
    # Analyze impact distribution
    high_impact = len([item for item in data if item.get('Impact') == 'High'])
    medium_impact = len([item for item in data if item.get('Impact') == 'Medium'])
    low_impact = len([item for item in data if item.get('Impact') == 'Low'])
    
    # Extract date range
    dates = [item['Date'] for item in data if 'Date' in item]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "Date range not available"
    
    if review_type.lower() == 'annual':
        return f"""# Annual Review Analysis

## Executive Summary
Successfully completed **{total_accomplishments} work items** during the review period ({date_range}), demonstrating consistent delivery and professional excellence across multiple domains.

**Impact Distribution:**
- High Impact: {high_impact} items ({high_impact/total_accomplishments*100:.1f}%)
- Medium Impact: {medium_impact} items ({medium_impact/total_accomplishments*100:.1f}%)
- Low Impact: {low_impact} items ({low_impact/total_accomplishments*100:.1f}%)

## Criterion Analysis

### 1. Communication
**Self Rating: 2 (Good)**

**How I Met This Criterion:**
Based on {total_accomplishments} completed work items, demonstrated clear communication through detailed technical documentation, comprehensive acceptance criteria, and thorough project specifications. All work items include clear descriptions and success criteria, indicating effective communication of requirements and deliverables.

### 2. Flexibility
**Self Rating: 2 (Good)**

**How I Met This Criterion:**
Successfully adapted to diverse project requirements and changing priorities across {total_accomplishments} work items. Maintained effectiveness while working on various technical domains and adjusting to evolving project needs throughout the review period.

### 3. Initiative
**Self Rating: 2 (Good)**

**How I Met This Criterion:**
Proactively completed {total_accomplishments} work items with {high_impact} classified as high impact, demonstrating self-direction and proactive problem-solving. Consistently identified and addressed project requirements before they became critical issues.

### 4. Member Service
**Self Rating: 2 (Good)**

**How I Met This Criterion:**
Delivered consistent service to internal stakeholders through reliable completion of {total_accomplishments} work items. Focused on meeting project requirements and supporting organizational objectives through quality deliverables.

### 5. Personal Credibility
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Demonstrated exceptional reliability with 100% completion rate across all {total_accomplishments} assigned work items. Consistently met commitments and followed through on all project responsibilities as evidenced by comprehensive success documentation.

### 6. Quality and Quantity of Work
**Self Rating: 3 (Excellent)**

**How I Met This Criterion:**
Achieved outstanding productivity with {total_accomplishments} completed work items while maintaining high quality standards. {high_impact} high-impact deliverables demonstrate significant value contribution to organizational objectives.

### 7. Teamwork
**Self Rating: 2 (Good)**

**How I Met This Criterion:**
Collaborated effectively on {total_accomplishments} work items, supporting team goals through consistent delivery and knowledge sharing. Contributed to collective success through reliable execution of assigned responsibilities.

## Overall Summary

Delivered exceptional performance with {total_accomplishments} successfully completed work items spanning {date_range}. Demonstrated strong professional competencies across all evaluation criteria, with particular excellence in personal credibility and work quality/quantity.

**Key Accomplishments:**
- {total_accomplishments} work items completed successfully
- {high_impact} high-impact deliverables providing significant organizational value
- Consistent delivery maintaining quality standards throughout the review period
- 100% completion rate demonstrating reliability and commitment

**Areas of Strength:**
- Exceptional reliability and follow-through on commitments
- High-volume delivery without compromising quality
- Effective adaptation to diverse project requirements
- Strong technical execution and problem-solving capabilities

_Analysis generated from {total_accomplishments} completed work items during the period {date_range}_
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