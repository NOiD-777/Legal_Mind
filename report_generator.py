import json
import csv
import io
from datetime import datetime
from typing import Dict, Any, List

class ReportGenerator:
    """Generates various formats of legal analysis reports"""
    
    def __init__(self):
        self.report_timestamp = datetime.now()
    
    def generate_text_report(self, analysis_results: Dict[str, Any], filename: str) -> str:
        """Generate a comprehensive text report"""
        
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("LEGAL DOCUMENT ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Document information
        report_lines.append("DOCUMENT INFORMATION")
        report_lines.append("-" * 30)
        report_lines.append(f"Filename: {filename}")
        report_lines.append(f"Analysis Date: {self.report_timestamp.strftime('%B %d, %Y at %I:%M %p')}")
        
        metadata = analysis_results.get('analysis_metadata', {})
        if metadata:
            report_lines.append(f"Analysis Depth: {metadata.get('analysis_depth', 'Unknown')}")
            report_lines.append(f"Focus Areas: {', '.join(metadata.get('focus_areas', []))}")
            report_lines.append(f"Document Length: {metadata.get('document_length', 'Unknown')} characters")
            report_lines.append(f"AI Model Used: {metadata.get('model_used', 'Unknown')}")
        
        report_lines.append("")
        
        # Executive Summary
        if analysis_results.get('executive_summary'):
            report_lines.append("EXECUTIVE SUMMARY")
            report_lines.append("-" * 30)
            report_lines.append(analysis_results['executive_summary'])
            report_lines.append("")
        
        # Overall Assessment
        report_lines.append("OVERALL ASSESSMENT")
        report_lines.append("-" * 30)
        report_lines.append(f"Overall Risk Score: {analysis_results.get('overall_risk_score', 'N/A')}/10")
        report_lines.append(f"Document Type: {analysis_results.get('document_type', 'Unknown')}")
        report_lines.append(f"Total Issues Identified: {len(analysis_results.get('issues', []))}")
        
        # Risk level breakdown
        issues = analysis_results.get('issues', [])
        risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for issue in issues:
            risk_level = issue.get('risk_level', 'Medium').title()
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1
        
        report_lines.append(f"  - High Risk Issues: {risk_counts['High']}")
        report_lines.append(f"  - Medium Risk Issues: {risk_counts['Medium']}")
        report_lines.append(f"  - Low Risk Issues: {risk_counts['Low']}")
        report_lines.append("")
        
        # Key Findings
        if analysis_results.get('key_findings'):
            report_lines.append("KEY FINDINGS")
            report_lines.append("-" * 30)
            for finding in analysis_results.get('key_findings', []):
                report_lines.append(f"• {finding}")
            report_lines.append("")
        
        # Detailed Issues Analysis
        if issues:
            report_lines.append("DETAILED ISSUES ANALYSIS")
            report_lines.append("-" * 30)
            
            # Group by risk level
            high_risk = [i for i in issues if i.get('risk_level', '').lower() == 'high']
            medium_risk = [i for i in issues if i.get('risk_level', '').lower() == 'medium']
            low_risk = [i for i in issues if i.get('risk_level', '').lower() == 'low']
            
            for risk_group, risk_name in [(high_risk, "HIGH RISK"), (medium_risk, "MEDIUM RISK"), (low_risk, "LOW RISK")]:
                if risk_group:
                    report_lines.append(f"\n{risk_name} ISSUES:")
                    report_lines.append("=" * len(f"{risk_name} ISSUES:"))
                    
                    for i, issue in enumerate(risk_group, 1):
                        report_lines.append(f"\n{i}. {issue.get('title', 'Untitled Issue')}")
                        report_lines.append(f"   Category: {issue.get('category', 'General')}")
                        report_lines.append(f"   Confidence: {issue.get('confidence', 0):.1%}")
                        report_lines.append(f"   Urgency: {issue.get('urgency', 'Medium')}")
                        
                        report_lines.append(f"\n   Description:")
                        report_lines.append(f"   {issue.get('description', 'No description available')}")
                        
                        if issue.get('potential_impact'):
                            report_lines.append(f"\n   Potential Impact:")
                            report_lines.append(f"   {issue.get('potential_impact')}")
                        
                        if issue.get('recommendations'):
                            report_lines.append(f"\n   Recommendations:")
                            for rec in issue.get('recommendations', []):
                                report_lines.append(f"   • {rec}")
                        
                        if issue.get('legal_citation'):
                            report_lines.append(f"\n   Legal Citation:")
                            report_lines.append(f"   {issue.get('legal_citation')}")
                        
                        report_lines.append("")
        
        # Compliance Flags
        if analysis_results.get('compliance_flags'):
            report_lines.append("COMPLIANCE CONSIDERATIONS")
            report_lines.append("-" * 30)
            for flag in analysis_results.get('compliance_flags', []):
                report_lines.append(f"• {flag}")
            report_lines.append("")
        
        # Positive Aspects
        if analysis_results.get('positive_aspects'):
            report_lines.append("POSITIVE ASPECTS")
            report_lines.append("-" * 30)
            for aspect in analysis_results.get('positive_aspects', []):
                report_lines.append(f"• {aspect}")
            report_lines.append("")
        
        # Next Steps
        if analysis_results.get('next_steps'):
            report_lines.append("RECOMMENDED NEXT STEPS")
            report_lines.append("-" * 30)
            for i, step in enumerate(analysis_results.get('next_steps', []), 1):
                report_lines.append(f"{i}. {step}")
            report_lines.append("")
        
        # Footer
        report_lines.append("=" * 80)
        report_lines.append("END OF REPORT")
        report_lines.append(f"Generated by LegalMind AI on {self.report_timestamp.strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def generate_json_report(self, analysis_results: Dict[str, Any], filename: str) -> str:
        """Generate a JSON format report"""
        
        report_data = {
            "report_metadata": {
                "filename": filename,
                "generated_at": self.report_timestamp.isoformat(),
                "report_type": "legal_document_analysis",
                "version": "1.0"
            },
            "analysis_results": analysis_results
        }
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)
    
    def generate_csv_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a CSV summary of issues"""
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Issue Title",
            "Category", 
            "Risk Level",
            "Confidence Score",
            "Urgency",
            "Description",
            "Potential Impact",
            "Recommendations",
            "Legal Citation"
        ])
        
        # Write issue data
        for issue in analysis_results.get('issues', []):
            recommendations = "; ".join(issue.get('recommendations', []))
            
            writer.writerow([
                issue.get('title', ''),
                issue.get('category', ''),
                issue.get('risk_level', ''),
                f"{issue.get('confidence', 0):.2%}",
                issue.get('urgency', ''),
                issue.get('description', ''),
                issue.get('potential_impact', ''),
                recommendations,
                issue.get('legal_citation', '')
            ])
        
        return output.getvalue()
    
    def generate_summary_stats(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the analysis"""
        
        issues = analysis_results.get('issues', [])
        
        # Risk level distribution
        risk_distribution = {'High': 0, 'Medium': 0, 'Low': 0}
        confidence_scores = []
        categories = {}
        
        for issue in issues:
            # Risk levels
            risk_level = issue.get('risk_level', 'Medium').title()
            if risk_level in risk_distribution:
                risk_distribution[risk_level] += 1
            
            # Confidence scores
            confidence_scores.append(issue.get('confidence', 0))
            
            # Categories
            category = issue.get('category', 'General')
            categories[category] = categories.get(category, 0) + 1
        
        # Calculate statistics
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        return {
            'total_issues': len(issues),
            'risk_distribution': risk_distribution,
            'average_confidence': avg_confidence,
            'category_distribution': categories,
            'overall_risk_score': analysis_results.get('overall_risk_score', 0),
            'high_priority_count': risk_distribution['High'],
            'requires_immediate_attention': risk_distribution['High'] > 0
        }
