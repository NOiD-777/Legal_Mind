import os
import json
import time
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import streamlit as st

class LegalAnalyzer:
    """Performs AI-powered legal document analysis using Google Gemini AI"""
    
    def __init__(self):
        # Using Google's Gemini Flash model for better rate limits on free tier
        self.model = "gemini-2.0-flash-lite"
        
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
            st.stop()
        
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(self.model)
        
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
            # Generate analysis prompt based on parameters
            prompt = self._create_analysis_prompt(text, analysis_depth, focus_areas)
            
            # Perform the analysis
            analysis_response = self._call_gemini_analysis(prompt)
            
            # Generate executive summary
            summary_response = self._generate_executive_summary(text, analysis_response)
            
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
                    'model_used': self.model
                }
            }
            
            return results
            
        except Exception as e:
            st.error(f"Error during legal analysis: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, text: str, analysis_depth: str, focus_areas: List[str]) -> str:
        """Create a structured prompt for legal document analysis"""
        
        # Base prompt
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
        
        # Add focus areas if specified
        if focus_areas:
            base_prompt += f"\nFocus Areas: Pay special attention to issues related to: {', '.join(focus_areas)}\n"
        
        # Depth-specific instructions
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
        
        # JSON format requirements
        base_prompt += """

Respond with a JSON object in the following format:
{
    "issues": [
        {
            "title": "Brief descriptive title of the issue",
            "description": "Detailed description of the legal issue or concern",
            "category": "Primary legal category (Contract Terms, Compliance, Liability, etc.)",
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
    
    def _call_gemini_analysis(self, prompt: str) -> Dict[str, Any]:
        """Make API call to Gemini for document analysis with retry logic"""
        
        max_retries = 3
        base_delay = 60  # Start with 60 seconds for rate limit errors
        
        for attempt in range(max_retries):
            try:
                # Create a more concise prompt to reduce token usage
                full_prompt = f"""You are a senior legal analyst. Analyze this legal document and identify potential issues.

{prompt}

Important: Respond with valid JSON only. Keep analysis concise but thorough."""

                response = self.client.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': 0.1,
                        'max_output_tokens': 2000,  # Reduced to stay within limits
                    }
                )
                
                # Extract text from response
                response_text = response.text
                
                # Clean the response to ensure it's valid JSON
                if response_text.startswith('```json'):
                    response_text = response_text.replace('```json', '').replace('```', '')
                response_text = response_text.strip()
                
                # Parse the JSON response
                analysis_result = json.loads(response_text)
                
                # Validate and clean the response
                return self._validate_analysis_response(analysis_result)
                
            except Exception as e:
                error_str = str(e)
                
                # Check if it's a rate limit error
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        st.warning(f"Rate limit reached. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}...")
                        time.sleep(delay)
                        continue
                    else:
                        # Return a simplified mock analysis for demonstration
                        return self._create_fallback_analysis()
                
                # For other errors, check if it's JSON parsing
                elif "json" in error_str.lower():
                    if attempt < max_retries - 1:
                        st.warning(f"Parsing error on attempt {attempt + 1}. Retrying...")
                        time.sleep(5)
                        continue
                    else:
                        return self._create_fallback_analysis()
                else:
                    raise Exception(f"Gemini API error: {error_str}")
        
        # If all retries failed, return fallback
        return self._create_fallback_analysis()
    
    def _generate_executive_summary(self, text: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an executive summary of the analysis"""
        
        summary_prompt = f"""
Based on the following legal document analysis, create an executive summary suitable for legal professionals and decision-makers.

Analysis Results:
{json.dumps(analysis_result, indent=2)}

Document Length: {len(text)} characters
Issues Found: {len(analysis_result.get('issues', []))}

Provide a JSON response with:
{{
    "executive_summary": "2-3 paragraph executive summary highlighting key findings, overall risk assessment, and critical areas requiring attention",
    "key_findings": ["Top 5 most important findings as bullet points"],
    "next_steps": ["5 specific recommended actions in order of priority"]
}}
"""
        
        try:
            # Skip executive summary if we're in rate limit mode
            if analysis_result.get('document_type') == 'Rate Limited Analysis':
                return {
                    "executive_summary": "Analysis could not be completed due to API rate limits. The legal document analyzer is designed to identify potential issues in contracts and legal documents using AI. Please try again when rate limits reset or consider using a shorter document.",
                    "key_findings": [
                        "API rate limits reached on free tier",
                        "System provides graceful error handling",
                        "Demonstration mode active"
                    ],
                    "next_steps": [
                        "Wait for rate limits to reset (typically 1 minute)",
                        "Try with a shorter document",
                        "Consider upgrading API plan for production use"
                    ]
                }
            
            # Create a concise summary prompt
            full_summary_prompt = f"""Legal consultant summary:

Analysis: {json.dumps(analysis_result, indent=2)[:1000]}...

Provide JSON with executive_summary, key_findings (5 items), next_steps (5 items)."""

            response = self.client.generate_content(
                full_summary_prompt,
                generation_config={
                    'temperature': 0.2,
                    'max_output_tokens': 800,  # Reduced for rate limits
                }
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '')
                
            return json.loads(response_text)
            
        except Exception as e:
            # Return default summary if API call fails
            return {
                "executive_summary": "Executive summary could not be generated due to processing error.",
                "key_findings": ["Analysis completed with identified issues"],
                "next_steps": ["Review individual issues for detailed recommendations"]
            }
    
    def _validate_analysis_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the analysis response"""
        
        # Ensure required fields exist
        if 'issues' not in response:
            response['issues'] = []
        
        # Validate each issue
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
            
            # Validate risk level
            if validated_issue['risk_level'].title() not in ['High', 'Medium', 'Low']:
                validated_issue['risk_level'] = 'Medium'
            
            # Ensure recommendations is a list
            if not isinstance(validated_issue['recommendations'], list):
                validated_issue['recommendations'] = [str(validated_issue['recommendations'])]
            
            validated_issues.append(validated_issue)
        
        response['issues'] = validated_issues
        
        # Validate overall risk score
        response['overall_risk_score'] = max(0, min(10, float(response.get('overall_risk_score', 5))))
        
        # Ensure other fields exist
        response['document_type'] = response.get('document_type', 'Unknown')
        response['compliance_flags'] = response.get('compliance_flags', [])
        response['positive_aspects'] = response.get('positive_aspects', [])
        
        return response
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create a fallback analysis when API is unavailable"""
        return {
            "issues": [
                {
                    "title": "API Rate Limit Reached",
                    "description": "The AI analysis service has reached its rate limit. This is a demonstration of how the system handles API limitations. In a production environment, you would upgrade to a paid tier for higher limits.",
                    "category": "System",
                    "risk_level": "Medium",
                    "confidence": 0.9,
                    "potential_impact": "Analysis cannot be completed at this time due to API limitations",
                    "recommendations": [
                        "Wait for rate limits to reset (typically 1 minute for free tier)",
                        "Consider upgrading to a paid API plan for higher rate limits",
                        "Use shorter documents to reduce token usage",
                        "Try again later when quotas have reset"
                    ],
                    "legal_citation": "Not applicable - technical limitation",
                    "urgency": "Low"
                },
                {
                    "title": "Document Analysis Demonstration",
                    "description": "This is a sample analysis result showing how the system would categorize and present legal issues when the AI service is available.",
                    "category": "General",
                    "risk_level": "Low",
                    "confidence": 0.8,
                    "potential_impact": "This is for demonstration purposes only",
                    "recommendations": [
                        "Upload a shorter document to test within rate limits",
                        "Try the analysis again in a few minutes",
                        "Consider using Quick analysis mode to reduce token usage"
                    ],
                    "legal_citation": "Demonstration only",
                    "urgency": "Low"
                }
            ],
            "overall_risk_score": 3.0,
            "document_type": "Rate Limited Analysis",
            "compliance_flags": ["API rate limits reached"],
            "positive_aspects": ["System gracefully handles API limitations", "Provides clear error messaging"]
        }
