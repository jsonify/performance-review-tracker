#!/usr/bin/env python3
"""
LLM Client for Performance Review Analysis

This module provides a unified interface for calling various LLM providers to analyze
work accomplishments against competency and annual review criteria.

Supports:
- OpenAI GPT models
- Anthropic Claude models
- Google Gemini models
- Azure OpenAI Service
- Local LLM APIs (Ollama, etc.)

Replaces the Roo Code VS Code extension integration with direct API calls.
"""

import json
import os
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging

# Set up logging
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Supported LLM providers."""
    REQUESTYAI = "requestyai"  # Unified provider for all models
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE_OPENAI = "azure_openai"
    OLLAMA = "ollama"
    ROOCODE = "roo_code"  # Fallback to existing system

@dataclass
class LLMResponse:
    """Response from LLM provider."""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None

class LLMClientError(Exception):
    """Base exception for LLM client errors."""
    pass

class LLMClient:
    """
    Unified LLM client that can work with multiple providers.
    
    This client provides a consistent interface for analyzing work accomplishments
    against performance review criteria using various LLM providers.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM client with configuration.
        
        Args:
            config: Configuration dictionary containing LLM settings
        """
        self.config = config.get("llm_integration", {})
        self.provider = LLMProvider(self.config.get("provider", "openai"))
        self.api_key = self.config.get("api_key", "")
        self.model = self.config.get("model", "")
        self.options = self.config.get("options", {})
        
        # Provider-specific settings
        self.temperature = self.options.get("temperature", 0.7)
        self.max_tokens = self.options.get("max_tokens", 4000)
        self.timeout = self.options.get("timeout", 120)
        
        # Initialize provider-specific client
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate client for the configured provider."""
        try:
            if self.provider == LLMProvider.REQUESTYAI:
                self._initialize_requestyai_client()
            elif self.provider == LLMProvider.OPENAI:
                self._initialize_openai_client()
            elif self.provider == LLMProvider.ANTHROPIC:
                self._initialize_anthropic_client()
            elif self.provider == LLMProvider.GOOGLE:
                self._initialize_google_client()
            elif self.provider == LLMProvider.AZURE_OPENAI:
                self._initialize_azure_openai_client()
            elif self.provider == LLMProvider.OLLAMA:
                self._initialize_ollama_client()
            elif self.provider == LLMProvider.ROOCODE:
                # Keep existing Roo Code functionality as fallback
                logger.info("Using Roo Code fallback - no client initialization needed")
                return
            else:
                raise LLMClientError(f"Unsupported provider: {self.provider}")
                
        except ImportError as e:
            logger.warning(f"Could not import required library for {self.provider}: {e}")
            if self.config.get("fallback_to_roo", False):
                logger.info("Falling back to Roo Code integration")
                self.provider = LLMProvider.ROOCODE
            else:
                raise LLMClientError(f"Provider {self.provider} not available and fallback disabled")
    
    def _initialize_openai_client(self):
        """Initialize OpenAI client."""
        try:
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
            if not self.model:
                self.model = "gpt-4o"  # Default to GPT-4o
        except ImportError:
            raise LLMClientError("OpenAI library not installed. Run: pip install openai")
    
    def _initialize_requestyai_client(self):
        """Initialize RequestyAI unified client."""
        try:
            import openai
            # RequestyAI uses OpenAI-compatible interface with their gateway
            self._client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://router.requesty.ai/v1"
            )
            if not self.model:
                self.model = "openai/gpt-4o-mini"  # Default RequestyAI model
        except ImportError:
            raise LLMClientError("OpenAI library not installed. Run: pip install openai")
    
    def _initialize_anthropic_client(self):
        """Initialize Anthropic Claude client."""
        try:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
            if not self.model:
                self.model = "claude-3-5-sonnet-20241022"  # Default to Claude 3.5 Sonnet
        except ImportError:
            raise LLMClientError("Anthropic library not installed. Run: pip install anthropic")
    
    def _initialize_google_client(self):
        """Initialize Google Gemini client."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            if not self.model:
                self.model = "gemini-1.5-pro"
            self._client = genai.GenerativeModel(self.model)
        except ImportError:
            raise LLMClientError("Google AI library not installed. Run: pip install google-generativeai")
    
    def _initialize_azure_openai_client(self):
        """Initialize Azure OpenAI client."""
        try:
            from openai import AzureOpenAI
            azure_endpoint = self.options.get("azure_endpoint")
            api_version = self.options.get("api_version", "2024-02-01")
            
            if not azure_endpoint:
                raise LLMClientError("Azure endpoint required for Azure OpenAI")
            
            self._client = AzureOpenAI(
                api_key=self.api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
            if not self.model:
                self.model = "gpt-4o"
        except ImportError:
            raise LLMClientError("OpenAI library not installed. Run: pip install openai")
    
    def _initialize_ollama_client(self):
        """Initialize Ollama client for local LLMs."""
        try:
            import ollama
            self._client = ollama.Client(host=self.options.get("ollama_host", "http://localhost:11434"))
            if not self.model:
                self.model = "llama3.2"  # Default local model
        except ImportError:
            raise LLMClientError("Ollama library not installed. Run: pip install ollama")
    
    def analyze_accomplishments(
        self, 
        accomplishments: List[Dict], 
        criteria: List[Dict], 
        review_type: str
    ) -> LLMResponse:
        """
        Analyze accomplishments against criteria using the configured LLM.
        
        Args:
            accomplishments: List of accomplishment dictionaries
            criteria: List of criteria dictionaries with expectations
            review_type: Type of review ("annual" or "competency")
            
        Returns:
            LLMResponse with analysis content
        """
        start_time = time.time()
        
        try:
            # Create the analysis prompt
            prompt = self._create_analysis_prompt(accomplishments, criteria, review_type)
            
            # Call the appropriate provider
            if self.provider == LLMProvider.ROOCODE:
                return self._fallback_to_roo_code(accomplishments, review_type)
            else:
                response_content = self._call_llm_provider(prompt)
            
            processing_time = time.time() - start_time
            
            return LLMResponse(
                content=response_content,
                provider=self.provider.value,
                model=self.model,
                processing_time=processing_time,
                success=True
            )
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            
            # Try fallback if enabled
            if self.config.get("fallback_to_roo", False):
                logger.info("Attempting Roo Code fallback...")
                return self._fallback_to_roo_code(accomplishments, review_type)
            
            return LLMResponse(
                content="",
                provider=self.provider.value,
                model=self.model,
                success=False,
                error_message=str(e)
            )
    
    def _create_analysis_prompt(
        self, 
        accomplishments: List[Dict], 
        criteria: List[Dict], 
        review_type: str
    ) -> str:
        """Create a comprehensive prompt for LLM analysis."""
        
        # Import keywords for better mapping guidance
        try:
            from .competency_keywords import COMPETENCY_KEYWORDS, map_accomplishments_to_competencies
        except ImportError:
            from competency_keywords import COMPETENCY_KEYWORDS, map_accomplishments_to_competencies
        
        # Create competency mapping for guidance
        competency_mapping = map_accomplishments_to_competencies(accomplishments, min_score=0.05)
        
        # Format accomplishments for the prompt with more detail
        accomplishments_text = "\n".join([
            f"**ACCOMPLISHMENT {i+1}: {acc.get('Title', 'Untitled')}**\n"
            f"• Date: {acc.get('Date', 'Unknown')}\n"
            f"• Description: {acc.get('Description', 'No description')}\n"
            f"• Acceptance Criteria: {acc.get('Acceptance Criteria', 'No criteria specified')}\n"
            f"• Impact Level: {acc.get('Impact', 'Medium')}\n"
            f"• Success Notes: {acc.get('Success Notes', 'Completed successfully')}\n"
            f"• Rating Justification: {acc.get('Rating Justification', 'Not provided')}\n"
            for i, acc in enumerate(accomplishments)
        ])
        
        # Format criteria for the prompt
        criteria_text = "\n".join([
            f"**{criterion['name']}**\n"
            f"Expectations:\n" + "\n".join([f"- {exp}" for exp in criterion['expectations']])
            for criterion in criteria
        ])
        
        if review_type.lower() == "annual":
            prompt = f"""You are an AI performance review analyst. Analyze the following work accomplishments against the Annual Review criteria.

## ACCOMPLISHMENTS TO ANALYZE
{accomplishments_text}

## ANNUAL REVIEW CRITERIA
{criteria_text}

## ANALYSIS REQUIREMENTS

For each criterion above, provide a comprehensive analysis following this exact format:

# [Criterion Name]

## Expectations
[List the specific expectations for this criterion from the criteria above]

## How I Met This Criterion
[Identify 2-4 specific examples from the accomplishments that demonstrate this criterion, with details]

## Areas for Improvement
[Based on the criterion expectations, identify 1-2 specific areas for growth]

## Improvement Plan
[Provide concrete, actionable steps for improvement in this area]

## Summary
[Write a concise paragraph summarizing performance, examples, areas for improvement, and growth plan]

## IMPORTANT INSTRUCTIONS:
- Use only the accomplishments provided above as evidence
- Reference specific accomplishments by title when giving examples
- Be specific and concrete in your analysis
- Focus on demonstrable results from the accomplishments
- Provide actionable improvement recommendations
- Rate performance based on evidence from accomplishments

Generate a complete analysis covering all {len(criteria)} criteria."""

        else:  # competency assessment
            # Create keyword mapping guidance for each competency
            keyword_guidance = "\n".join([
                f"**{comp_name}**: Look for accomplishments containing keywords like: {', '.join(keywords[:8])}"
                for comp_name, keywords in COMPETENCY_KEYWORDS.items()
            ])
            
            # Create accomplishment mapping guidance
            mapping_guidance = "\n".join([
                f"**{comp_name}**: Most relevant accomplishments appear to be: " + 
                (", ".join([f"#{i+1}" for i, acc in enumerate(accomplishments) if acc in comp_accs]) if comp_accs else "No direct matches - analyze all accomplishments for this competency")
                for comp_name, comp_accs in competency_mapping.items()
            ])
            
            prompt = f"""You are an AI competency assessment analyst with expertise in evidence-based evaluation. Analyze the work accomplishments against the Competency Assessment criteria using specific examples and technical details.

## ACCOMPLISHMENTS TO ANALYZE
{accomplishments_text}

## COMPETENCY ASSESSMENT CRITERIA
{criteria_text}

## KEYWORD MAPPING GUIDANCE
Use these keywords to identify relevant accomplishments for each competency:
{keyword_guidance}

## SUGGESTED ACCOMPLISHMENT MAPPING
Based on keyword analysis, these accomplishments are most relevant to each competency:
{mapping_guidance}

## ANALYSIS REQUIREMENTS

For EACH competency, provide a comprehensive analysis following this EXACT format:

# [Competency Name]

## Rating: [1-5] ([Rating Level])

## Expectations Met
[List specific expectations from the criteria that are demonstrated by the accomplishments]

## Evidence from Accomplishments  
[Provide 2-4 SPECIFIC examples from the accomplishments that demonstrate this competency. Include:
- Accomplishment title and number (e.g., "Accomplishment #3: Fix Invalid Directory Structures")
- Specific technical details from the description
- Quantifiable results from Success Notes
- How this demonstrates the competency expectations]

## Evidence Analysis
[Analyze how the evidence supports the assigned rating level. Reference specific accomplishment details that justify the rating.]

## Areas for Growth
[Based on gaps between current evidence and higher rating levels, identify 1-2 specific areas for development]

## Development Recommendations
[Provide 2-3 concrete, actionable steps to advance to the next competency level]

## COMPETENCY RATING SCALE:
1. **Learning** - Beginning to apply with guidance (minimal evidence)
2. **Developing** - Building proficiency with occasional support (some evidence)
3. **Practicing** - Consistent competency independently (solid evidence)
4. **Mastering** - Advanced proficiency, guides others (strong evidence + leadership)
5. **Leading** - Expert level, drives innovation (exceptional evidence + transformation)

## CRITICAL INSTRUCTIONS:
- MUST reference specific accomplishment titles and numbers in evidence
- MUST include technical details from accomplishment descriptions
- MUST use quantifiable results from Success Notes when available  
- MUST differentiate analysis based on the ACTUAL accomplishment content
- MUST assign ratings based on demonstrated evidence, not assumptions
- MUST analyze ALL {len(criteria)} competencies even if no obvious matches
- For competencies without clear matches, explain why evidence is limited

Generate analysis covering ALL {len(criteria)} competencies with specific evidence from the {len(accomplishments)} accomplishments provided."""

        return prompt
    
    def _call_llm_provider(self, prompt: str) -> str:
        """Call the appropriate LLM provider with the prompt."""
        
        if self.provider == LLMProvider.REQUESTYAI:
            return self._call_requestyai(prompt)
        elif self.provider == LLMProvider.OPENAI:
            return self._call_openai(prompt)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._call_anthropic(prompt)
        elif self.provider == LLMProvider.GOOGLE:
            return self._call_google(prompt)
        elif self.provider == LLMProvider.AZURE_OPENAI:
            return self._call_azure_openai(prompt)
        elif self.provider == LLMProvider.OLLAMA:
            return self._call_ollama(prompt)
        else:
            raise LLMClientError(f"Provider {self.provider} not implemented")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert performance review analyst who provides thorough, evidence-based evaluations."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    
    def _call_requestyai(self, prompt: str) -> str:
        """Call RequestyAI unified gateway API."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert performance review analyst who provides thorough, evidence-based evaluations."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        response = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system="You are an expert performance review analyst who provides thorough, evidence-based evaluations.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _call_google(self, prompt: str) -> str:
        """Call Google Gemini API."""
        generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens,
        }
        
        system_instruction = "You are an expert performance review analyst who provides thorough, evidence-based evaluations."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        response = self._client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        return response.text
    
    def _call_azure_openai(self, prompt: str) -> str:
        """Call Azure OpenAI API."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert performance review analyst who provides thorough, evidence-based evaluations."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama local LLM API."""
        response = self._client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert performance review analyst who provides thorough, evidence-based evaluations."},
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        )
        return response['message']['content']
    
    def _fallback_to_roo_code(self, accomplishments: List[Dict], review_type: str) -> LLMResponse:
        """Fallback to existing Roo Code integration."""
        logger.info("Using Roo Code fallback for analysis")
        
        try:
            # Use the manual analysis since Roo Code subprocess isn't set up for this context
            try:
                from .llm_analyzer import generate_manual_analysis
            except ImportError:
                from llm_analyzer import generate_manual_analysis
            
            # Create a temporary data file for the manual analysis function
            import tempfile
            import json
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(accomplishments, temp_file, indent=2)
                temp_file_path = temp_file.name
            
            try:
                manual_content = generate_manual_analysis(temp_file_path, review_type)
                return LLMResponse(
                    content=manual_content,
                    provider="roo_code_fallback",
                    model="manual_analysis",
                    success=True
                )
            finally:
                # Clean up temp file
                import os
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Roo Code fallback failed: {e}")
            return LLMResponse(
                content="Analysis fallback failed. Please check the configuration.",
                provider="roo_code_fallback",
                model="manual_analysis",
                success=False,
                error_message=str(e)
            )
    
    def test_connection(self) -> bool:
        """Test the connection to the configured LLM provider."""
        try:
            if self.provider == LLMProvider.ROOCODE:
                return True  # Can't easily test Roo Code connection
            
            # Simple test prompt
            test_prompt = "Hello! Please respond with 'Connection successful' to test the API."
            
            response_content = self._call_llm_provider(test_prompt)
            return "successful" in response_content.lower() or len(response_content) > 0
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_supported_models(self) -> List[str]:
        """Get list of supported models for the current provider."""
        model_lists = {
            LLMProvider.REQUESTYAI: [
                # OpenAI models via RequestyAI
                "openai/gpt-4o",
                "openai/gpt-4o-mini",
                "openai/gpt-4-turbo",
                "openai/gpt-3.5-turbo",
                # Anthropic models via RequestyAI
                "anthropic/claude-3-5-sonnet-20241022",
                "anthropic/claude-3-5-haiku-20241022",
                "anthropic/claude-3-opus-20240229",
                # Coding-optimized models
                "coding/claude-4-sonnet",
                "openai/o1-preview",
                "openai/o1-mini",
                # Google models via RequestyAI
                "google/gemini-1.5-pro",
                "google/gemini-1.5-flash",
                "google/gemini-pro",
                # Meta models via RequestyAI
                "meta/llama-3.2-90b",
                "meta/llama-3.1-70b",
                "meta/llama-3.2-11b",
                # Mistral models
                "mistral/mistral-large-2407",
                "mistral/codestral-latest",
                # Cohere models
                "cohere/command-r-plus",
                "cohere/command-r",
                # Additional specialized models
                "deepseek/deepseek-coder",
                "x-ai/grok-beta"
            ],
            LLMProvider.OPENAI: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            LLMProvider.ANTHROPIC: ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
            LLMProvider.GOOGLE: ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"],
            LLMProvider.AZURE_OPENAI: ["gpt-4o", "gpt-4-turbo", "gpt-35-turbo"],
            LLMProvider.OLLAMA: ["llama3.2", "llama3.1", "mistral", "codellama"],
            LLMProvider.ROOCODE: ["roo_code"]
        }
        
        return model_lists.get(self.provider, [])


def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    """
    Factory function to create an LLM client from configuration.
    
    Args:
        config: Full application configuration
        
    Returns:
        Initialized LLM client
    """
    return LLMClient(config)