# LegalMind - Legal Document Analysis

⚖️ AI-powered legal document analysis using Google Gemini AI

## Overview

LegalMind is a Streamlit-based application that performs comprehensive analysis of legal documents including contracts, agreements, and other legal texts. It uses Google's Gemini AI to identify potential issues, assess risks, and provide actionable recommendations.

## Features

- 📄 **Multi-format Support**: Analyze PDF, DOCX, and TXT documents
- 🔍 **Deep Analysis**: Identifies legal issues across multiple categories
- ⚠️ **Risk Assessment**: Severity scoring and confidence ratings
- 📊 **Visual Reports**: Interactive charts and comprehensive PDF reports
- 🎯 **Smart Recommendations**: Actionable suggestions for each identified issue

## Setup

### Prerequisites

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

### Configuration

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Add your Google Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

**Important**: Never commit your `.env` file to version control. It's already listed in `.gitignore`.

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

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
