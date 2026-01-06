# LegalMind - Multi-Model Comparison Guide

## How to Compare Models

### Step 1: Configure API Keys
Add your API keys to `.env`:
```bash
GEMINI_API_KEY=your_key_here          # Required
OPENAI_API_KEY=your_key_here          # Optional
ANTHROPIC_API_KEY=your_key_here       # Optional
```

### Step 2: Upload Document
Upload any legal document (PDF, DOCX, or TXT)

### Step 3: Select "Compare Models" Mode
In the sidebar, choose the "Compare Models" radio button

### Step 4: Select Models to Compare
Choose 2-4 models from the available options:
- ✅ Models with configured API keys will be available
- ⚠️ Models without API keys will be hidden

### Step 5: Run Comparison
Click "Analyze Document" and wait for all models to complete

## What You'll Get

### 📊 Accuracy Scores Tab
- Comparative accuracy scores (0-100%)
- Bar chart visualization
- Best performing model highlighted

**Accuracy Calculation:**
- 50% based on average confidence levels
- 30% based on number of issues found
- 20% based on risk assessment consistency

### ⚖️ Consensus Issues Tab
- Issues identified by multiple models
- Shows which models agree on each issue
- Sorted by number of models in agreement

### ⚡ Performance Tab
- Response time comparison
- Token usage per model
- Number of issues found
- Average confidence scores
- Visual charts for each metric

### 📋 Individual Results Tab
- Detailed results from each model
- Top 5 issues per model
- Risk scores and metrics
- Full issue descriptions

## Example Use Cases

### Use Case 1: Validation
Compare results from 2-3 models to validate findings and increase confidence in the analysis.

### Use Case 2: Cost vs Quality
Compare a free model (Gemini Flash) with paid models (GPT-4o, Claude) to see if the extra cost provides better insights.

### Use Case 3: Speed vs Accuracy
Test fast models (Haiku, GPT-4o Mini) against slower, more thorough models (GPT-4o, Claude Sonnet).

### Use Case 4: Specialized Analysis
Compare models on documents requiring specific expertise (e.g., employment law, IP protection).

## Tips for Best Results

1. **Start with 2 models** for faster comparisons
2. **Use Quick analysis** for initial testing
3. **Try Comprehensive mode** when you need detailed findings
4. **Focus on consensus issues** - these are likely the most important
5. **Consider cost** - paid models may provide better results but at higher cost

## Model Characteristics

### Gemini 2.0 Flash
- ⚡ Fastest response
- 💰 Free tier available
- 🎯 Good for quick checks
- ⚠️ May have rate limits

### GPT-4o
- 🧠 Strong reasoning
- 📊 Comprehensive analysis
- 💰 Moderate cost
- ⚡ Good balance of speed/quality

### Claude 3.5 Sonnet
- 🎓 Best for complex documents
- 📖 Excellent at understanding context
- 💰 Moderate cost
- 🔍 Thorough analysis

### GPT-4o Mini / Claude Haiku
- ⚡⚡ Very fast
- 💰 Low cost
- ✅ Good for quick analysis
- 🎯 Efficient for simple documents

## Accuracy Score Interpretation

- **90-100%**: Excellent - High confidence, consistent findings
- **80-89%**: Very Good - Reliable analysis with minor variations
- **70-79%**: Good - Solid analysis, may need validation
- **60-69%**: Fair - Consider comparing with another model
- **Below 60%**: Review carefully - May need re-analysis

## Next Steps

After comparison:
1. Review consensus issues first (high priority)
2. Check model-specific findings (may catch unique issues)
3. Use the best-performing model for detailed follow-up
4. Export reports for documentation

## Troubleshooting

**"API key not found"**
- Add the required API key to your `.env` file
- Restart the Streamlit app

**"Select at least 2 models"**
- Choose 2 or more models from the multiselect dropdown
- Ensure you have API keys configured for selected models

**Slow comparison**
- Use "Quick" analysis mode
- Reduce number of models
- Try shorter documents first

**Different results**
- Normal - models have different approaches
- Focus on consensus issues for reliability
- Higher accuracy scores = more consistent results
