# LLM Integration Guide

This guide explains how to set up and use the new LLM integration feature that replaces the Roo Code VS Code extension.

## Overview

The Performance Review Tracker now supports direct integration with multiple LLM providers for analyzing work accomplishments against competency and annual review criteria. This eliminates the need for VS Code and provides more reliable, automated analysis.

## Supported Providers

### 1. RequestyAI Unified Gateway (🌟 Recommended)
- **Models**: All major models from OpenAI, Anthropic, Google, Meta, Mistral, Cohere
- **Best for**: Production use, cost optimization, maximum reliability
- **Benefits**: 
  - Single API key for all providers
  - Up to 40% cost savings
  - Intelligent routing and fallback
  - 99.99% uptime SLA
- **Cost**: Optimized pricing across all providers
- **Setup**: Sign up at [app.requesty.ai](https://app.requesty.ai)

### 2. OpenAI
- **Models**: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **Best for**: High-quality analysis, reliable performance
- **Cost**: Pay-per-use API pricing

### 3. Anthropic Claude
- **Models**: Claude-3.5-Sonnet, Claude-3.5-Haiku, Claude-3-Opus
- **Best for**: Detailed analysis, complex reasoning
- **Cost**: Pay-per-use API pricing

### 4. Google Gemini  
- **Models**: Gemini-1.5-Pro, Gemini-1.5-Flash, Gemini-1.0-Pro
- **Best for**: Cost-effective analysis
- **Cost**: Generous free tier, then pay-per-use

### 5. Azure OpenAI
- **Models**: GPT-4o, GPT-4-turbo, GPT-35-turbo
- **Best for**: Enterprise deployments, compliance requirements
- **Cost**: Enterprise pricing

### 5. Ollama (Local)
- **Models**: Llama3.2, Llama3.1, Mistral, CodeLlama
- **Best for**: Privacy, no API costs
- **Cost**: Free (requires local GPU/CPU resources)

### 6. Roo Code (Fallback)
- **Best for**: Existing users who want to maintain VS Code integration
- **Note**: Original system maintained as fallback option

## Setup Instructions

### Step 1: Install Dependencies

Choose and install the dependency for your preferred provider:

```bash
# For OpenAI
pip install openai>=1.0.0

# For Anthropic Claude
pip install anthropic>=0.8.0

# For Google Gemini
pip install google-generativeai>=0.3.0

# For Ollama (local)
pip install ollama>=0.1.0

# Or install all providers
pip install -r requirements-llm.txt
```

### Step 2: Get API Keys

#### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Add billing information to your account
4. Note: GPT-4 requires a paid account

#### Anthropic Claude
1. Visit [Anthropic Console](https://console.anthropic.com/settings/keys)
2. Create an API key
3. Add billing information for usage beyond free tier

#### Google Gemini
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Enable the Generative AI API

#### Azure OpenAI
1. Create an Azure OpenAI resource
2. Get the API key and endpoint from Azure portal
3. Deploy a model (GPT-4o recommended)

#### Ollama (Local)
1. Install Ollama: [https://ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama3.2`
3. Start Ollama service: `ollama serve`

### Step 3: Configure Your Provider

Edit `config.json` and set up your chosen provider:

#### OpenAI Configuration
```json
{
  "llm_integration": {
    "provider": "openai",
    "api_key": "sk-proj-your-key-here",
    "model": "gpt-4o",
    "options": {
      "temperature": 0.7,
      "max_tokens": 4000,
      "timeout": 120
    }
  }
}
```

#### Anthropic Configuration
```json
{
  "llm_integration": {
    "provider": "anthropic",
    "api_key": "sk-ant-api03-your-key-here",
    "model": "claude-3-5-sonnet-20241022",
    "options": {
      "temperature": 0.7,
      "max_tokens": 4000
    }
  }
}
```

#### Google Gemini Configuration
```json
{
  "llm_integration": {
    "provider": "google",
    "api_key": "AIyour-key-here",
    "model": "gemini-1.5-pro",
    "options": {
      "temperature": 0.7,
      "max_tokens": 4000
    }
  }
}
```

#### Azure OpenAI Configuration
```json
{
  "llm_integration": {
    "provider": "azure_openai",
    "api_key": "your-azure-key",
    "model": "gpt-4o",
    "options": {
      "azure_endpoint": "https://your-resource.openai.azure.com/",
      "api_version": "2024-02-01",
      "temperature": 0.7,
      "max_tokens": 4000
    }
  }
}
```

#### Ollama Configuration
```json
{
  "llm_integration": {
    "provider": "ollama",
    "model": "llama3.2",
    "options": {
      "ollama_host": "http://localhost:11434",
      "temperature": 0.7,
      "max_tokens": 4000
    }
  }
}
```

### Step 4: Test Your Configuration

```bash
# Test configuration and LLM connection
python src/main.py --test-config

# Run a sample analysis
python src/main.py --source csv --file data/sample_accomplishments.csv --type competency
```

## Usage

Once configured, the LLM integration works automatically with all existing commands:

```bash
# Generate competency assessment using LLM
python src/main.py --source ado --type competency

# Generate annual review using LLM
python src/main.py --source ado --type annual --year 2025

# Use CSV data with LLM analysis
python src/main.py --source csv --file data/accomplishments.csv --type competency
```

## Analysis Quality

The LLM integration provides:

1. **Detailed Criterion Analysis**: Each accomplishment is analyzed against specific criteria
2. **Evidence-Based Ratings**: Ratings justified with specific examples from your work
3. **Actionable Improvement Plans**: Concrete suggestions for professional development
4. **Comprehensive Coverage**: Analysis covers all criteria (7 for annual, 13 for competency)

## Cost Considerations

### Estimated Token Usage
- **Competency Assessment**: ~3,000-5,000 tokens
- **Annual Review**: ~4,000-6,000 tokens
- **Cost per analysis**: $0.01-0.05 (varies by provider and model)

### Cost Optimization Tips
1. Use GPT-4o-mini instead of GPT-4o for cost savings
2. Use Google Gemini for free tier availability
3. Use Ollama for completely free local processing
4. Set reasonable `max_tokens` limits

## Troubleshooting

### Common Issues

#### "LLM provider connection failed"
- Check your API key is correct and active
- Verify you have sufficient account credits
- For Ollama, ensure the service is running

#### "Provider X not available"
- Install the required dependency: `pip install provider-name`
- Check that the library is properly installed

#### Analysis returns empty results
- Check your API key has the right permissions
- Verify your account has sufficient credits
- The system will automatically fall back to manual analysis

#### Rate limiting errors
- Add delays between requests using the `timeout` setting
- Consider using a different provider
- Check your API tier limits

### Fallback Behavior

The system is designed with multiple fallback layers:

1. **Primary**: Configured LLM provider
2. **Secondary**: Manual analysis (same as before)
3. **Tertiary**: Roo Code (if `fallback_to_roo: true`)

## Advanced Configuration

### Custom Prompts
You can modify the analysis prompts by editing `src/llm_client.py` in the `_create_analysis_prompt` method.

### Provider-Specific Options
Each provider supports additional options in the `options` section:

```json
{
  "llm_integration": {
    "provider": "openai",
    "options": {
      "temperature": 0.7,      // Creativity level (0-1)
      "max_tokens": 4000,      // Response length limit
      "timeout": 120,          // Request timeout (seconds)
      "top_p": 0.9,           // Nucleus sampling
      "frequency_penalty": 0   // Repetition penalty
    }
  }
}
```

### Multiple Provider Setup
You can switch between providers by changing the configuration:

```bash
# Create separate config files
cp config.json config-openai.json
cp config.json config-claude.json

# Use different configs
python src/main.py --config config-openai.json --type competency
python src/main.py --config config-claude.json --type competency
```

## Migration from Roo Code

If you're currently using Roo Code:

1. **Keep existing workflow**: Set `"provider": "roo_code"` to maintain current behavior
2. **Gradual transition**: Set `"fallback_to_roo": true` to use LLM with Roo Code fallback
3. **Full migration**: Choose an LLM provider and set `"fallback_to_roo": false`

The analysis format and output remain the same, so existing reports and templates continue to work.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your configuration with `--test-config`
3. Check that you have the required dependencies installed
4. Review the console output for specific error messages

The system is designed to be robust - if LLM analysis fails, it will automatically fall back to the proven manual analysis system.