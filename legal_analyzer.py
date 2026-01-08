import os
import json
import time
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import streamlit as st
from openai import OpenAI
from anthropic import Anthropic

# Groq is optional; handle gracefully if not installed
try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency
    Groq = None

class LegalAnalyzer:
    """Performs AI-powered legal document analysis using multiple AI models"""
    
    # Available models configuration
    AVAILABLE_MODELS = {
        # Google Gemini (latest previews + 2.5 family)
        "gemini-3-pro-preview": {"provider": "google", "name": "Gemini 3 Pro (Preview)", "cost": "medium"},
        "gemini-3-flash-preview": {"provider": "google", "name": "Gemini 3 Flash (Preview)", "cost": "low"},
        "gemini-2.5-flash": {"provider": "google", "name": "Gemini 2.5 Flash", "cost": "low"},
        "gemini-2.5-flash-lite": {"provider": "google", "name": "Gemini 2.5 Flash Lite", "cost": "free"},
        "gemini-2.5-pro": {"provider": "google", "name": "Gemini 2.5 Pro", "cost": "medium"},

        # OpenAI (4o family)
        "gpt-4o": {"provider": "openai", "name": "GPT-4o", "cost": "medium"},
        "gpt-4o-mini": {"provider": "openai", "name": "GPT-4o Mini", "cost": "low"},

        # Anthropic (3.5 family)
        "claude-3-5-sonnet-20241022": {"provider": "anthropic", "name": "Claude 3.5 Sonnet", "cost": "medium"},
        "claude-3-5-haiku-20241022": {"provider": "anthropic", "name": "Claude 3.5 Haiku", "cost": "low"},

        # Groq (popular free GroqCloud models)
        "llama-3.1-70b-versatile": {"provider": "groq", "name": "Llama 3.1 70B Versatile", "cost": "free"},
        "llama-3.1-8b-instant": {"provider": "groq", "name": "Llama 3.1 8B Instant", "cost": "free"},
        "mixtral-8x7b-32768": {"provider": "groq", "name": "Mixtral 8x7B", "cost": "free"},
    }
    
    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        self.model = model_name
        self.provider = self.AVAILABLE_MODELS.get(model_name, {}).get("provider", "google")
        
        # Initialize appropriate client based on provider
        self._initialize_clients()
        
        # Performance tracking
        self.performance_metrics = {
            "response_time": 0,
            "tokens_used": 0,
            "issues_found": 0,
            "confidence_avg": 0
        }
        
        # Legal categories for issue classification
        self.legal_categories = [
            "Contract Terms",
            "Compliance",
            "Liability",
            "Intellectual Property", 
            "Employment Law",
            "Privacy & Data Protection",
            "Financial Terms",
            "Dispute Resolution",
            "Regulatory Requirements",
            "Risk Management"
        ]
    
    def _initialize_clients(self):
        """Initialize API clients for all available providers"""
        self.clients = {}
        
        # Google Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.clients["google"] = genai
        
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.clients["openai"] = OpenAI(api_key=openai_key)
        
        # Anthropic Claude
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.clients["anthropic"] = Anthropic(api_key=anthropic_key)
        
        # Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            if Groq is None:
                st.warning("Groq SDK not installed. Run 'pip install groq' to enable Groq models.")
            else:
                self.clients["groq"] = Groq(api_key=groq_key)
        
        # Check if required provider is available
        if self.provider not in self.clients:
            st.warning(f"API key not found for {self.provider}. Please add it to your .env file.")
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of models that have API keys configured"""
        available = []
        
        if os.getenv("GEMINI_API_KEY"):
            available.extend([k for k, v in cls.AVAILABLE_MODELS.items() if v["provider"] == "google"])
        if os.getenv("OPENAI_API_KEY"):
            available.extend([k for k, v in cls.AVAILABLE_MODELS.items() if v["provider"] == "openai"])
        if os.getenv("ANTHROPIC_API_KEY"):
            available.extend([k for k, v in cls.AVAILABLE_MODELS.items() if v["provider"] == "anthropic"])
        if os.getenv("GROQ_API_KEY"):
            available.extend([k for k, v in cls.AVAILABLE_MODELS.items() if v["provider"] == "groq"])
        
        return available if available else ["gemini-3-flash-preview"]
    
    def analyze_document(self, text: str, analysis_depth: str, focus_areas: List[str], filename: str) -> Dict[str, Any]:
        """
        Analyze a legal document for potential issues and risks
        
        Args:
            text: The document text to analyze
            analysis_depth: Level of analysis (Comprehensive, Quick, Focused)
            focus_areas: Specific legal areas to focus on
            filename: Name of the document being analyzed
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            start_time = time.time()
            
            # Generate analysis prompt based on parameters
            prompt = self._create_analysis_prompt(text, analysis_depth, focus_areas)
            
            # Perform the analysis using selected model
            analysis_response = self._call_ai_analysis(prompt)
            
            # Generate executive summary
            summary_response = self._generate_executive_summary(text, analysis_response)
            
            # Calculate performance metrics
            self.performance_metrics["response_time"] = time.time() - start_time
            self.performance_metrics["issues_found"] = len(analysis_response.get('issues', []))
            
            # Calculate average confidence
            issues = analysis_response.get('issues', [])
            if issues:
                self.performance_metrics["confidence_avg"] = sum(i.get('confidence', 0) for i in issues) / len(issues)
            
            # Combine results
            results = {
                **analysis_response,
                'executive_summary': summary_response.get('executive_summary', ''),
                'key_findings': summary_response.get('key_findings', []),
                'next_steps': summary_response.get('next_steps', []),
                'analysis_metadata': {
                    'filename': filename,
                    'analysis_depth': analysis_depth,
                    'focus_areas': focus_areas,
                    'document_length': len(text),
                    'model_used': self.model,
                    'provider': self.provider,
                    'response_time': self.performance_metrics["response_time"],
                    'timestamp': time.time()
                },
                'performance_metrics': self.performance_metrics
            }
            
            return results
            
        except Exception as e:
            st.error(f"Error during legal analysis with {self.model}: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, text: str, analysis_depth: str, focus_areas: List[str]) -> str:
        """Create a structured prompt for legal document analysis"""
        
        base_prompt = f"""
You are an expert legal analyst tasked with analyzing a legal document for potential issues, risks, and areas of concern. 

Document to analyze:
{text[:8000]}{'...' if len(text) > 8000 else ''}

Analysis Requirements:
- Identify specific legal issues, risks, and problematic clauses
- Categorize each issue into appropriate legal domains
- Assess risk levels (High, Medium, Low) for each issue
- Provide confidence scores (0.0 to 1.0) for each identified issue
- Give specific recommendations for addressing each issue
- Consider potential legal implications and consequences

Analysis Depth: {analysis_depth}
"""
        
        if focus_areas:
            base_prompt += f"\nFocus Areas: Pay special attention to issues related to: {', '.join(focus_areas)}\n"
        
        if analysis_depth == "Comprehensive":
            base_prompt += """
Provide a thorough analysis including:
- Detailed examination of all clauses and terms
- Cross-referencing with relevant legal standards
- Potential edge cases and unusual scenarios
- Regulatory compliance considerations
"""
        elif analysis_depth == "Quick":
            base_prompt += """
Provide a focused analysis on:
- Most critical and obvious issues
- High-risk areas requiring immediate attention
- Major red flags and concerning clauses
"""
        elif analysis_depth == "Focused":
            base_prompt += """
Provide targeted analysis on:
- Issues specifically related to the selected focus areas
- Specialized legal concerns in those domains
- Industry-specific compliance requirements
"""
        
        base_prompt += """

Respond with a JSON object in the following format:
{
    "issues": [
        {
            "title": "Brief descriptive title of the issue",
            "description": "Detailed description of the legal issue or concern",
            "category": "Primary legal category",
            "risk_level": "High/Medium/Low",
            "confidence": 0.85,
            "potential_impact": "Description of potential consequences",
            "recommendations": ["Specific action item 1", "Specific action item 2"],
            "legal_citation": "Relevant laws or regulations if applicable",
            "urgency": "Immediate/High/Medium/Low"
        }
    ],
    "overall_risk_score": 7.5,
    "document_type": "Identified document type",
    "compliance_flags": ["List of potential compliance issues"],
    "positive_aspects": ["Well-drafted clauses or protective terms"]
}

Ensure all confidence scores are between 0.0 and 1.0, and the overall_risk_score is between 0 and 10.
"""
        
        return base_prompt
    
    def _call_ai_analysis(self, prompt: str) -> Dict[str, Any]:
        """Make API call to selected AI model for document analysis"""
        
        if self.provider == "google":
            return self._call_gemini_analysis(prompt)
        elif self.provider == "openai":
            return self._call_openai_analysis(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic_analysis(prompt)
        elif self.provider == "groq":
            return self._call_groq_analysis(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_gemini_analysis(self, prompt: str) -> Dict[str, Any]:
        """Call Google Gemini API"""
        try:
            client = genai.GenerativeModel(self.model)
            response = client.generate_content(
                prompt,
                generation_config={'temperature': 0.1, 'max_output_tokens': 2000}
            )
            
            if hasattr(response, 'usage_metadata'):
                self.performance_metrics["tokens_used"] = getattr(response.usage_metadata, 'total_token_count', 0)
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return self._validate_analysis_response(json.loads(response_text))
        except Exception as e:
            st.warning(f"Gemini API error: {str(e)}")
            return self._create_fallback_analysis()
    
    def _call_openai_analysis(self, prompt: str) -> Dict[str, Any]:
        """Call OpenAI GPT API"""
        try:
            client = self.clients.get("openai")
            if not client:
                raise ValueError("OpenAI client not initialized")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert legal analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            self.performance_metrics["tokens_used"] = response.usage.total_tokens
            
            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return self._validate_analysis_response(json.loads(response_text))
        except Exception as e:
            st.warning(f"OpenAI API error: {str(e)}")
            return self._create_fallback_analysis()
    
    def _call_anthropic_analysis(self, prompt: str) -> Dict[str, Any]:
        """Call Anthropic Claude API"""
        try:
            client = self.clients.get("anthropic")
            if not client:
                raise ValueError("Anthropic client not initialized")
            
            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            self.performance_metrics["tokens_used"] = response.usage.input_tokens + response.usage.output_tokens
            
            response_text = response.content[0].text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return self._validate_analysis_response(json.loads(response_text))
        except Exception as e:
            st.warning(f"Anthropic API error: {str(e)}")
            return self._create_fallback_analysis()
    
    def _call_groq_analysis(self, prompt: str) -> Dict[str, Any]:
        """Call Groq API"""
        try:
            client = self.clients.get("groq")
            if not client:
                raise ValueError("Groq client not initialized")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert legal analyst. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            self.performance_metrics["tokens_used"] = response.usage.total_tokens if hasattr(response, 'usage') else 0
            
            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return self._validate_analysis_response(json.loads(response_text))
        except Exception as e:
            st.warning(f"Groq API error: {str(e)}")
            return self._create_fallback_analysis()
            return self._create_fallback_analysis()
    
    def _generate_executive_summary(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an executive summary of the analysis"""
        
        if analysis_result.get('document_type') == 'Rate Limited Analysis':
            return {
                "executive_summary": "Analysis could not be completed due to API limitations.",
                "key_findings": ["API limitations encountered"],
                "next_steps": ["Retry analysis", "Try shorter document"]
            }
        
        summary_prompt = f"""
Based on the following legal document analysis, create an executive summary.

Analysis: {json.dumps(analysis_result, indent=2)[:1000]}...

Provide JSON with:
- executive_summary: 2-3 paragraph summary
- key_findings: Array of 5 key findings
- next_steps: Array of 5 recommended actions
"""
        
        try:
            if self.provider == "google":
                client = genai.GenerativeModel(self.model)
                response = client.generate_content(summary_prompt, generation_config={'temperature': 0.2, 'max_output_tokens': 800})
                response_text = response.text.strip()
            elif self.provider == "openai":
                client = self.clients.get("openai")
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": summary_prompt}],
                    temperature=0.2,
                    max_tokens=800
                )
                response_text = response.choices[0].message.content.strip()
            elif self.provider == "anthropic":
                client = self.clients.get("anthropic")
                response = client.messages.create(
                    model=self.model,
                    max_tokens=800,
                    messages=[{"role": "user", "content": summary_prompt}]
                )
                response_text = response.content[0].text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
        except:
            return {
                "executive_summary": "Summary generation unavailable.",
                "key_findings": ["Analysis completed"],
                "next_steps": ["Review detailed findings"]
            }
    
    def _validate_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the analysis response"""
        
        if 'issues' not in response:
            response['issues'] = []
        
        validated_issues = []
        for issue in response.get('issues', []):
            validated_issue = {
                'title': issue.get('title', 'Untitled Issue'),
                'description': issue.get('description', 'No description provided'),
                'category': issue.get('category', 'General'),
                'risk_level': issue.get('risk_level', 'Medium'),
                'confidence': max(0.0, min(1.0, float(issue.get('confidence', 0.5)))),
                'potential_impact': issue.get('potential_impact', 'Impact assessment not provided'),
                'recommendations': issue.get('recommendations', []),
                'legal_citation': issue.get('legal_citation', ''),
                'urgency': issue.get('urgency', 'Medium')
            }
            
            if validated_issue['risk_level'].title() not in ['High', 'Medium', 'Low']:
                validated_issue['risk_level'] = 'Medium'
            
            if not isinstance(validated_issue['recommendations'], list):
                validated_issue['recommendations'] = [str(validated_issue['recommendations'])]
            
            validated_issues.append(validated_issue)
        
        response['issues'] = validated_issues
        response['overall_risk_score'] = max(0, min(10, float(response.get('overall_risk_score', 5))))
        response['document_type'] = response.get('document_type', 'Unknown')
        response['compliance_flags'] = response.get('compliance_flags', [])
        response['positive_aspects'] = response.get('positive_aspects', [])
        
        return response
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create a fallback analysis when API is unavailable"""
        return {
            "issues": [{
                "title": "API Unavailable",
                "description": f"The {self.provider} API is currently unavailable. Please check your API key configuration.",
                "category": "System",
                "risk_level": "Medium",
                "confidence": 0.9,
                "potential_impact": "Analysis cannot be completed",
                "recommendations": ["Verify API key", "Check rate limits", "Try different model"],
                "legal_citation": "N/A",
                "urgency": "Low"
            }],
            "overall_risk_score": 3.0,
            "document_type": "Rate Limited Analysis",
            "compliance_flags": ["API limitations"],
            "positive_aspects": ["System handles errors gracefully"]
        }


class ModelComparator:
    """Compare analysis results from multiple AI models"""
    
    @staticmethod
    def compare_models(text: str, models: List[str], analysis_depth: str, focus_areas: List[str], filename: str) -> Dict[str, Any]:
        """Run analysis with multiple models and compare results"""
        
        results = {}
        comparison_metrics = {
            "models_compared": len(models),
            "comparison_timestamp": time.time()
        }
        
        with st.spinner("Running multi-model comparison..."):
            for model in models:
                st.write(f"Analyzing with {LegalAnalyzer.AVAILABLE_MODELS.get(model, {}).get('name', model)}...")
                
                try:
                    analyzer = LegalAnalyzer(model_name=model)
                    result = analyzer.analyze_document(text, analysis_depth, focus_areas, filename)
                    results[model] = result
                except Exception as e:
                    st.error(f"Error with {model}: {str(e)}")
                    results[model] = {"error": str(e)}
        
        # Calculate comparison metrics
        comparison_metrics["accuracy_scores"] = ModelComparator._calculate_accuracy_scores(results)
        comparison_metrics["consensus_issues"] = ModelComparator._find_consensus_issues(results)
        comparison_metrics["performance_comparison"] = ModelComparator._compare_performance(results)
        
        return {
            "individual_results": results,
            "comparison_metrics": comparison_metrics
        }
    
    @staticmethod
    def _calculate_accuracy_scores(results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate relative accuracy scores based on confidence and consensus"""
        accuracy_scores = {}
        
        for model, result in results.items():
            if "error" in result:
                accuracy_scores[model] = 0.0
                continue
            
            # Factors: average confidence, number of issues found, risk assessment consistency
            avg_confidence = result.get('performance_metrics', {}).get('confidence_avg', 0)
            issues_count = result.get('performance_metrics', {}).get('issues_found', 0)
            risk_score = result.get('overall_risk_score', 5) / 10
            
            # Weighted accuracy score
            accuracy = (avg_confidence * 0.5) + (min(issues_count / 10, 1.0) * 0.3) + (risk_score * 0.2)
            accuracy_scores[model] = round(accuracy * 100, 2)
        
        return accuracy_scores
    
    @staticmethod
    def _find_consensus_issues(results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find issues that multiple models agree on"""
        all_issues = {}
        
        for model, result in results.items():
            if "error" in result:
                continue
            
            for issue in result.get('issues', []):
                category = issue.get('category', 'Unknown')
                risk_level = issue.get('risk_level', 'Unknown')
                key = f"{category}_{risk_level}"
                
                if key not in all_issues:
                    all_issues[key] = {
                        "category": category,
                        "risk_level": risk_level,
                        "count": 0,
                        "models": []
                    }
                
                all_issues[key]["count"] += 1
                all_issues[key]["models"].append(model)
        
        # Return issues found by multiple models
        consensus = [v for v in all_issues.values() if v["count"] > 1]
        return sorted(consensus, key=lambda x: x["count"], reverse=True)
    
    @staticmethod
    def _compare_performance(results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Compare performance metrics across models"""
        comparison = {}
        
        for model, result in results.items():
            if "error" in result:
                continue
            
            metrics = result.get('performance_metrics', {})
            comparison[model] = {
                "response_time": round(metrics.get('response_time', 0), 2),
                "tokens_used": metrics.get('tokens_used', 0),
                "issues_found": metrics.get('issues_found', 0),
                "avg_confidence": round(metrics.get('confidence_avg', 0), 3)
            }
        
        return comparison
