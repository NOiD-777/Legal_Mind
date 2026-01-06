# Quick Start Guide - Multi-Model Features

## 🚀 Getting Started in 3 Steps

### Step 1: Run the Application
```bash
streamlit run app.py
```

### Step 2: Upload a Document
- Click "Browse files" in the sidebar
- Select a PDF, DOCX, or TXT legal document
- Wait for validation ✅

### Step 3: Choose Your Analysis Mode

#### Option A: Single Model Analysis
```
1. Select "Single Model" radio button
2. Choose your preferred model from dropdown
3. Click "Analyze Document"
```

#### Option B: Compare Multiple Models
```
1. Select "Compare Models" radio button
2. Select 2-4 models from multiselect
3. Click "Analyze Document"
4. Review comparison in 4 tabs
```

## 📊 Understanding the Results

### Single Model Results
- **Risk Score**: Overall risk rating (0-10)
- **Issues Found**: Number of concerns identified
- **Avg Confidence**: How confident the AI is
- **Tokens Used**: API usage metric
- **Response Time**: How long analysis took

### Comparison Results

#### Tab 1: 📊 Accuracy Scores
Shows which model performed best:
- Bar chart of accuracy scores
- Sorted from best to worst
- Winner highlighted in green

#### Tab 2: ⚖️ Consensus Issues
Issues multiple models agree on:
- Sorted by agreement level
- Shows which models found each issue
- These are likely the most important!

#### Tab 3: ⚡ Performance
Speed and efficiency comparison:
- Response time comparison
- Token usage (cost indicator)
- Issues detected
- Confidence levels

#### Tab 4: 📋 Individual Results
Detailed view per model:
- Risk scores
- Top 5 issues per model
- Performance metrics
- Full issue descriptions

## 🎯 What Each Model is Best For

### Use Gemini 2.0 Flash When:
- ✅ You want quick results
- ✅ Testing the system
- ✅ You have rate limits
- ✅ Cost is a concern

### Use GPT-4o When:
- ✅ You need comprehensive analysis
- ✅ Document is complex
- ✅ Quality over speed matters
- ✅ You have OpenAI credits

### Use Claude 3.5 Sonnet When:
- ✅ Document requires deep reasoning
- ✅ Complex legal language
- ✅ Need thorough explanations
- ✅ You have Anthropic credits

### Use Comparison Mode When:
- ✅ Validating important findings
- ✅ High-stakes documents
- ✅ Testing model performance
- ✅ Want maximum confidence

## 💡 Pro Tips

### Tip 1: Start Fast
Begin with Gemini Flash or GPT-4o Mini for quick overview, then use a more powerful model for detailed analysis.

### Tip 2: Use Comparison Wisely
For critical documents, compare 2-3 models and focus on consensus issues.

### Tip 3: Check API Keys
The app shows which APIs are configured in the sidebar. Add keys to `.env` to unlock more models.

### Tip 4: Choose Analysis Depth
- **Quick**: For initial review (faster, fewer tokens)
- **Comprehensive**: For thorough analysis (slower, more detailed)
- **Focused**: For specific legal areas

### Tip 5: Interpret Accuracy Scores
- 90-100%: Excellent confidence
- 80-89%: Very reliable
- 70-79%: Good, validate if critical
- Below 70%: Consider additional review

## 🔑 Adding More API Keys

### To Add OpenAI (GPT-4):
1. Get key from https://platform.openai.com/api-keys
2. Open `.env` file
3. Add: `OPENAI_API_KEY=sk-...`
4. Restart the app
5. GPT-4 models now available!

### To Add Anthropic (Claude):
1. Get key from https://console.anthropic.com/
2. Open `.env` file
3. Add: `ANTHROPIC_API_KEY=sk-ant-...`
4. Restart the app
5. Claude models now available!

## 📈 Reading the Charts

### Accuracy Bar Chart
- **Higher is better**
- Green = Best performer
- Based on confidence + consistency

### Response Time Chart
- **Lower is better**
- Shows speed of each model
- Important for large documents

### Token Usage Chart
- **Lower is better** (for cost)
- Shows API consumption
- Helps estimate costs

### Issues Found Chart
- **More isn't always better**
- Compare with confidence
- Look for consensus

## ⚠️ Common Questions

**Q: Which model is most accurate?**
A: It varies by document type. Use comparison mode to find out!

**Q: Why do models give different results?**
A: Each AI has different training and approaches. Consensus issues are most reliable.

**Q: How much do API calls cost?**
A: Gemini Flash is free. Others charge per token - check pricing pages.

**Q: Can I use only free models?**
A: Yes! Gemini Flash is powerful and free.

**Q: How do I know if an issue is real?**
A: Higher confidence scores and consensus across models indicate reliability.

## 🎓 Example Workflow

### For a New Contract:
1. **First Pass**: Use Gemini Flash (Quick mode)
2. **Review**: Check major issues found
3. **Deep Dive**: Use GPT-4o or Claude (Comprehensive mode)
4. **Validate**: Compare 2-3 models for critical clauses
5. **Report**: Export findings for legal review

### For Routine Documents:
1. **Single Model**: Use Gemini Flash or GPT-4o Mini
2. **Quick Mode**: Fast analysis
3. **Review**: Check flagged issues
4. **Done**: Export report if needed

### For Critical Documents:
1. **Comparison Mode**: Use 3 models
2. **Comprehensive Mode**: Full analysis
3. **Focus**: On consensus issues
4. **Review**: All individual findings
5. **Report**: Detailed export with all findings

## 📞 Need Help?

- Check README.md for detailed documentation
- See MODEL_COMPARISON_GUIDE.md for comparison features
- Review ENHANCEMENT_SUMMARY.md for technical details

## ✅ Quick Checklist

Before analyzing:
- [ ] Document uploaded and validated
- [ ] API keys configured (check sidebar)
- [ ] Analysis mode selected
- [ ] Model(s) chosen
- [ ] Analysis depth selected

After analyzing:
- [ ] Review risk score
- [ ] Check confidence levels
- [ ] Read consensus issues (if comparing)
- [ ] Review recommendations
- [ ] Export report if needed

---

**You're all set! Start analyzing legal documents with AI-powered insights! 🚀⚖️**
