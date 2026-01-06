import streamlit as st
import os
import tempfile
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from document_processor import DocumentProcessor
from legal_analyzer import LegalAnalyzer
from report_generator import ReportGenerator
from utils import validate_file, format_confidence_score

# Configure page
st.set_page_config(
    page_title="LegalMind - Legal Document Analysis",
    page_icon="⚖️",
    layout="wide"
)

# Initialize components
@st.cache_resource
def initialize_components():
    processor = DocumentProcessor()
    analyzer = LegalAnalyzer()
    report_gen = ReportGenerator()
    return processor, analyzer, report_gen

def main():
    # Header
    st.title("⚖️ LegalMind - Legal Document Analysis")
    st.markdown("**AI-Powered Legal Risk Assessment and Issue Identification**")
    st.divider()
    
    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'filename' not in st.session_state:
        st.session_state.filename = None
    
    # Initialize components
    try:
        processor, analyzer, report_gen = initialize_components()
    except Exception as e:
        st.error(f"Failed to initialize application components: {str(e)}")
        st.stop()
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Choose a legal document",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, Word Document, or Text file (Max 200MB)"
        )
        
        if uploaded_file:
            # Validate file
            validation_result = validate_file(uploaded_file)
            if not validation_result['valid']:
                st.error(validation_result['message'])
            else:
                st.success(f"✅ File validated: {uploaded_file.name}")
                
                # Analysis options
                st.subheader("Analysis Options")
                analysis_depth = st.selectbox(
                    "Analysis Depth",
                    ["Comprehensive", "Quick", "Focused"],
                    help="Comprehensive: Full analysis with detailed insights\nQuick: Fast overview of major issues\nFocused: Specific legal area analysis"
                )
                
                focus_areas = st.multiselect(
                    "Focus Areas (Optional)",
                    ["Contract Terms", "Compliance", "Liability", "Intellectual Property", 
                     "Employment Law", "Privacy & Data Protection", "Financial Terms", "Dispute Resolution"],
                    help="Select specific areas to focus the analysis on"
                )
                
                # Analyze button
                if st.button("🔍 Analyze Document", type="primary"):
                    analyze_document(uploaded_file, processor, analyzer, analysis_depth, focus_areas)
        
        # Download sample documents section - always visible
        st.divider()
        st.subheader("📥 Sample Documents")
        st.write("Download test documents to try the analyzer:")
        
        # Check if sample files exist and provide download buttons
        import os
        if os.path.exists("short_test_contract.docx"):
            with open("short_test_contract.docx", "rb") as file:
                st.download_button(
                    label="📄 Download Short Test Contract",
                    data=file.read(),
                    file_name="short_test_contract.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Short contract with legal issues for testing"
                )
        
        if os.path.exists("sample_legal_contract.docx"):
            with open("sample_legal_contract.docx", "rb") as file:
                st.download_button(
                    label="📄 Download Full Sample Contract",
                    data=file.read(),
                    file_name="sample_legal_contract.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Comprehensive contract for advanced testing"
                )
        
        if os.path.exists("sample_employment_agreement.docx"):
            with open("sample_employment_agreement.docx", "rb") as file:
                st.download_button(
                    label="📄 Download Employment Agreement",
                    data=file.read(),
                    file_name="sample_employment_agreement.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    help="Employment agreement with potential issues"
                )
    
    # Main content area
    if st.session_state.analysis_results is None:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### Welcome to LegalMind
            
            Upload a legal document to get started with AI-powered analysis that identifies:
            
            - **Potential Legal Issues** - Contract terms, compliance gaps, liability concerns
            - **Risk Assessment** - Confidence-scored risk levels for each issue
            - **Issue Categorization** - Organized findings by legal domain
            - **Actionable Insights** - Specific recommendations and next steps
            - **Professional Reports** - Export-ready analysis summaries
            
            **Supported Formats:** PDF, Word Documents (.docx), Text Files (.txt)
            """)
    else:
        # Display analysis results
        display_analysis_results(report_gen)

def analyze_document(uploaded_file, processor, analyzer, analysis_depth, focus_areas):
    """Process and analyze the uploaded document"""
    
    with st.spinner("Processing document..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                tmp_file_path = tmp_file.name
            
            # Extract text from document
            text_content = processor.extract_text(tmp_file_path, uploaded_file.type)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            if not text_content or len(text_content.strip()) < 50:
                st.error("Document appears to be empty or text could not be extracted.")
                return
            
            # Store document info
            st.session_state.document_text = text_content
            st.session_state.filename = uploaded_file.name
            
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            return
    
    with st.spinner("Analyzing legal content..."):
        try:
            # Perform legal analysis
            analysis_results = analyzer.analyze_document(
                text_content, 
                analysis_depth, 
                focus_areas,
                uploaded_file.name
            )
            
            # Store results
            st.session_state.analysis_results = analysis_results
            
            st.success("✅ Analysis completed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

def display_analysis_results(report_gen):
    """Display the analysis results in organized tabs"""
    
    results = st.session_state.analysis_results
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Issues Found", 
            len(results.get('issues', [])),
            help="Total number of legal issues identified"
        )
    
    with col2:
        high_risk_count = sum(1 for issue in results.get('issues', []) if issue.get('risk_level', '').lower() == 'high')
        st.metric(
            "High Risk Issues", 
            high_risk_count,
            help="Issues requiring immediate attention"
        )
    
    with col3:
        avg_confidence = sum(issue.get('confidence', 0) for issue in results.get('issues', [])) / max(len(results.get('issues', [])), 1)
        st.metric(
            "Avg Confidence", 
            f"{avg_confidence:.1%}",
            help="Average confidence score for identified issues"
        )
    
    with col4:
        overall_risk = results.get('overall_risk_score', 0)
        st.metric(
            "Overall Risk Score", 
            f"{overall_risk}/10",
            help="Comprehensive risk assessment score"
        )
    
    st.divider()
    
    # Tabs for detailed results
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Issues Overview", "📊 Risk Analysis", "📋 Categorized Issues", "📄 Document Summary", "📁 Export Report"])
    
    with tab1:
        display_issues_overview(results)
    
    with tab2:
        display_risk_analysis(results)
    
    with tab3:
        display_categorized_issues(results)
    
    with tab4:
        display_document_summary(results)
    
    with tab5:
        display_export_options(results, report_gen)

def display_issues_overview(results):
    """Display overview of all identified issues"""
    
    issues = results.get('issues', [])
    
    if not issues:
        st.info("No legal issues were identified in this document.")
        return
    
    st.subheader("Identified Legal Issues")
    
    for i, issue in enumerate(issues, 1):
        # Create expandable issue card
        risk_color = {
            'high': '🔴',
            'medium': '🟡', 
            'low': '🟢'
        }.get(issue.get('risk_level', '').lower(), '⚪')
        
        with st.expander(f"{risk_color} {issue.get('title', f'Issue {i}')} - {issue.get('risk_level', 'Unknown').title()} Risk"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write("**Description:**")
                st.write(issue.get('description', 'No description available'))
                
                if issue.get('potential_impact'):
                    st.write("**Potential Impact:**")
                    st.write(issue.get('potential_impact'))
                
                if issue.get('recommendations'):
                    st.write("**Recommendations:**")
                    for rec in issue.get('recommendations', []):
                        st.write(f"• {rec}")
            
            with col2:
                st.write("**Risk Level:**")
                st.write(issue.get('risk_level', 'Unknown').title())
                
                st.write("**Confidence:**")
                confidence = issue.get('confidence', 0)
                st.progress(confidence, text=f"{confidence:.1%}")
                
                st.write("**Category:**")
                st.write(issue.get('category', 'General'))

def display_risk_analysis(results):
    """Display risk analysis with visualizations"""
    
    issues = results.get('issues', [])
    
    if not issues:
        st.info("No risk data available.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        
        # Risk level distribution
        risk_counts = {}
        for issue in issues:
            risk_level = issue.get('risk_level', 'Unknown').title()
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
        
        if risk_counts:
            fig_pie = px.pie(
                values=list(risk_counts.values()),
                names=list(risk_counts.keys()),
                color_discrete_map={
                    'High': '#ff4444',
                    'Medium': '#ffaa00', 
                    'Low': '#44ff44',
                    'Unknown': '#cccccc'
                }
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Confidence Scores")
        
        # Confidence score distribution
        confidence_data = []
        for i, issue in enumerate(issues):
            confidence_data.append({
                'Issue': f"Issue {i+1}",
                'Confidence': issue.get('confidence', 0),
                'Risk Level': issue.get('risk_level', 'Unknown').title()
            })
        
        if confidence_data:
            df_confidence = pd.DataFrame(confidence_data)
            fig_bar = px.bar(
                df_confidence,
                x='Issue',
                y='Confidence',
                color='Risk Level',
                color_discrete_map={
                    'High': '#ff4444',
                    'Medium': '#ffaa00',
                    'Low': '#44ff44',
                    'Unknown': '#cccccc'
                }
            )
            fig_bar.update_layout(yaxis_title='Confidence Score', xaxis_title='Issues')
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Risk timeline if available
    st.subheader("Priority Matrix")
    
    # Create impact vs probability matrix
    matrix_data = []
    for i, issue in enumerate(issues):
        # Estimate impact and probability from confidence and risk level
        risk_map = {'low': 1, 'medium': 2, 'high': 3}
        impact = risk_map.get(issue.get('risk_level', '').lower(), 2)
        probability = issue.get('confidence', 0.5) * 3
        
        matrix_data.append({
            'Issue': issue.get('title', f'Issue {i+1}'),
            'Impact': impact,
            'Probability': probability,
            'Risk Level': issue.get('risk_level', 'Unknown').title()
        })
    
    if matrix_data:
        df_matrix = pd.DataFrame(matrix_data)
        fig_scatter = px.scatter(
            df_matrix,
            x='Probability',
            y='Impact',
            color='Risk Level',
            size=[1] * len(matrix_data),
            hover_data=['Issue'],
            color_discrete_map={
                'High': '#ff4444',
                'Medium': '#ffaa00',
                'Low': '#44ff44',
                'Unknown': '#cccccc'
            }
        )
        fig_scatter.update_layout(
            xaxis_title='Probability/Confidence',
            yaxis_title='Impact Level',
            xaxis=dict(range=[0, 3]),
            yaxis=dict(range=[0, 4])
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

def display_categorized_issues(results):
    """Display issues organized by category"""
    
    issues = results.get('issues', [])
    
    if not issues:
        st.info("No categorized issues available.")
        return
    
    # Group issues by category
    categories = {}
    for issue in issues:
        category = issue.get('category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append(issue)
    
    st.subheader("Issues by Category")
    
    for category, category_issues in categories.items():
        st.markdown(f"### {category}")
        
        # Category summary
        high_risk_in_category = sum(1 for issue in category_issues if issue.get('risk_level', '').lower() == 'high')
        st.write(f"**{len(category_issues)} issues found** ({high_risk_in_category} high risk)")
        
        # Display issues in this category
        for issue in category_issues:
            risk_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue.get('risk_level', '').lower(), '⚪')
            
            with st.container():
                st.markdown(f"{risk_emoji} **{issue.get('title', 'Untitled Issue')}**")
                st.write(issue.get('description', 'No description available'))
                
                if issue.get('recommendations'):
                    st.write("*Recommendations:*")
                    for rec in issue.get('recommendations', []):
                        st.write(f"  • {rec}")
                
                st.markdown("---")

def display_document_summary(results):
    """Display document summary and key findings"""
    
    st.subheader("Document Analysis Summary")
    
    # Document metadata
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Document Information:**")
        st.write(f"• Filename: {st.session_state.filename}")
        st.write(f"• Analysis Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        st.write(f"• Document Length: {len(st.session_state.document_text or '')} characters")
        st.write(f"• Issues Identified: {len(results.get('issues', []))}")
    
    with col2:
        st.write("**Risk Assessment:**")
        overall_risk = results.get('overall_risk_score', 0)
        st.write(f"• Overall Risk Score: {overall_risk}/10")
        
        risk_level = "Low"
        if overall_risk >= 7:
            risk_level = "High"
        elif overall_risk >= 4:
            risk_level = "Medium"
        
        st.write(f"• Risk Level: {risk_level}")
        st.write(f"• Requires Review: {'Yes' if overall_risk >= 4 else 'No'}")
    
    # Executive summary
    if results.get('executive_summary'):
        st.subheader("Executive Summary")
        st.write(results.get('executive_summary'))
    
    # Key findings
    if results.get('key_findings'):
        st.subheader("Key Findings")
        for finding in results.get('key_findings', []):
            st.write(f"• {finding}")
    
    # Next steps
    if results.get('next_steps'):
        st.subheader("Recommended Next Steps")
        for step in results.get('next_steps', []):
            st.write(f"• {step}")

def display_export_options(results, report_gen):
    """Display export options for the analysis report"""
    
    st.subheader("Export Analysis Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Formats:**")
        
        # Generate JSON report
        if st.button("📄 Download JSON Report"):
            json_report = report_gen.generate_json_report(results, st.session_state.filename)
            st.download_button(
                label="Download JSON",
                data=json_report,
                file_name=f"legal_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Generate CSV summary
        if st.button("📊 Download CSV Summary"):
            csv_report = report_gen.generate_csv_report(results)
            st.download_button(
                label="Download CSV",
                data=csv_report,
                file_name=f"legal_issues_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.write("**Report Contents:**")
        st.write("• Executive summary")
        st.write("• Detailed issue analysis")
        st.write("• Risk assessments")
        st.write("• Recommendations")
        st.write("• Document metadata")
    
    # Detailed text report
    st.subheader("Detailed Text Report")
    
    text_report = report_gen.generate_text_report(results, st.session_state.filename)
    st.text_area("Report Preview", text_report, height=300, disabled=True)
    
    st.download_button(
        label="📋 Download Full Text Report",
        data=text_report,
        file_name=f"legal_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

if __name__ == "__main__":
    main()
