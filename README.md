# LegalMind - Legal Document Analysis

⚖️ AI-powered legal document analysis with multi-model support and comparison

## Overview

LegalMind is a Streamlit-based application that performs comprehensive analysis of legal documents including contracts, agreements, and other legal texts. It supports multiple AI models (Google Gemini, OpenAI GPT-4, Anthropic Claude) and allows you to compare their performance and accuracy.

## Features

- 🤖 **Multi-Model Support**: Choose from Gemini, GPT-4o, or Claude models
- 📊 **Model Comparison**: Run analysis with multiple models simultaneously
- 📈 **Accuracy Scoring**: See performance metrics and confidence levels for each model
- 📄 **Multi-format Support**: Analyze PDF, DOCX, and TXT documents
- 🔍 **Deep Analysis**: Identifies legal issues across multiple categories
- ⚠️ **Risk Assessment**: Severity scoring and confidence ratings
- 📊 **Visual Reports**: Interactive charts and comprehensive comparisons
- 🎯 **Smart Recommendations**: Actionable suggestions for each identified issue

## Setup

##At least one AI API key:
  - Google Gemini (free tier available)
  - OpenAI GPT-4 (optional)
  - Anthropic Claude (optional)

- Python 3.11 or higher
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd legal
```

2. Install dependencies:
```bash
pip install -e .
```
 (already created)

2. Add your AI API keys to `.env`:
```
# Required - Google Gemini (free tier available)
GEMINI_API_KEY=your_gemini_key_here

# Optional - for model comparison features
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

**Important**: Never commit your `.env` file to version control. It's already listed in `.gitignore`.

### Getting API Keys

**Google Gemini** (Free tier available):
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key

**OpenAI GPT-4** (Optional, for comparison):
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an account and add billing
3. Generate a new API key

**Anthropic Claude** (Optional, for comparison):
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account
3. Generate an API key/makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
   - **Single Model**: Use one AI model for analysis
   - **Compare Models**: Run analysis with multiple models and compare results
3. **Select AI Model(s)**:
   - Gemini 2.0 Flash (free, fast)
   - Gemini 1.5 Pro (advanced)
   - GPT-4o (powerful, requires API key)
   - GPT-4o Mini (efficient)
   - Claude 3.5 Sonnet (advanced reasoning)
   - Claude 3.5 Haiku (fast)
4. **Choose Analysis Depth**:
   - Quick Mode: Faster analysis with focused insights
   - Comprehensive Mode: Detailed analysis with full findings
   - Focused Mode: Specific legal area analysis with multi-model support
├── legal_analyzer.py         # Multi-model AI analysis engine with comparison
├── document_processor.py     # Document parsing and processing
├── report_generator.py       # PDF report generation
├── utils.py                  # Utility functions
├── pyproject.toml           # Project dependencies
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## AI Models

The application supports the following models:

| Model | Provider | Speed | Cost | Best For |
|-------|----------|-------|------|----------|
| Gemini 2.0 Flash | Google | ⚡⚡⚡ | Free | Quick analysis, testing |
| Gemini 1.5 Pro | Google | ⚡⚡ | Low | Detailed analysis |
| GPT-4o | OpenAI | ⚡⚡ | Medium | Comprehensive insights |
| GPT-4o Mini | OpenAI | ⚡⚡⚡ | Low | Fast, cost-effective |
| Claude 3.5 Sonnet | Anthropic | ⚡⚡ | Medium | Complex reasoning |
| Claude 3.5 Haiku | Anthropic | ⚡⚡⚡ | Low | Quick turnaround |

## Model Comparison Features

When using comparison mode, you get:

- **Accuracy Scores**: Calculated based on confidence levels and consistency
- **Consensus Issues**: Issues identified by multiple models
- **Performance Metrics**: Response time, token usage, and efficiency
- **Side-by-Side Results**: Compare findings from each model

The application will open in your default web browser at `http://localhost:8501`.
openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models
- `
### Analysis Workflow

1. **Upload Document**: Select a legal document (PDF, DOCX, or TXT)
2. **Choose Analysis Mode**: 
   - Quick Mode: Faster analysis with focused insights
   - Deep Mode: Comprehensive analysis with detailed findings
3. **Review Results**: View identified issues, risk assessments, and recommendations
4. **Generate Report**: Download a comprehensive PDF report

## Project Structure

```
legal/
├── app.py                    # Main Streamlit application
├── legal_analyzer.py         # AI-powered legal analysis engine
├── document_processor.py     # Document parsing and processing
├── report_generator.py       # PDF report generation
├── utils.py                  # Utility functions
├── pyproject.toml           # Project dependencies
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Legal Categories Analyzed

- Contract Terms
- Compliance
- Liability
- Intellectual Property
- Employment Law
- Data Privacy
- Dispute Resolution
- Indemnification
- Termination Clauses
- Payment Terms

## Security

- **API Keys**: All sensitive keys are stored in `.env` and excluded from version control
- **Local Processing**: Documents are processed locally and not stored permanently
- **Temporary Files**: Uploaded files are stored in temporary directories and cleaned up after analysis

## Dependencies

- `streamlit` - Web application framework
- `google-generativeai` - Google Gemini AI integration
- `pdfplumber` - PDF text extraction
- `python-docx` - DOCX document processing
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations
- `python-dotenv` - Environment variable management

See [pyproject.toml](pyproject.toml) for complete dependency list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license here]

## Disclaimer

This tool is designed to assist with legal document analysis but should not be considered a replacement for professional legal advice. Always consult with a qualified attorney for legal matters.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
