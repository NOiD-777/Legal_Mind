import streamlit as st
import os
import tempfile
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from legal_analyzer import LegalAnalyzer, ModelComparator
from report_generator import ReportGenerator
from utils import validate_file, format_confidence_score

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="LegalMind - Legal Document Analysis",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'filename' not in st.session_state:
        st.session_state.filename = None
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = "single"

# Initialize components
@st.cache_resource
def initialize_components():
    processor = DocumentProcessor()
    report_gen = ReportGenerator()
    return processor, report_gen

def main():
    initialize_session_state()
    
    # Header
    st.title("⚖️ LegalMind - Multi-Model Legal Document Analysis")
    st.markdown("**AI-Powered Legal Risk Assessment with Model Comparison**")
    st.divider()
    
    # Initialize components
    try:
        processor, report_gen = initialize_components()
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
                
                # Analysis Mode
                st.subheader("🤖 Analysis Mode")
                analysis_mode = st.radio(
                    "Select Mode",
                    ["single", "compare"],
                    format_func=lambda x: "Single Model" if x == "single" else "Compare Models",
                    help="Single: Use one model\nCompare: Run analysis with multiple models and compare results"
                )
                st.session_state.analysis_mode = analysis_mode
                
                # Get available models
                available_models = LegalAnalyzer.get_available_models()
                model_names = {m: LegalAnalyzer.AVAILABLE_MODELS[m]['name'] for m in available_models}
                
                if analysis_mode == "single":
                    # Single model selection
                    selected_model = st.selectbox(
                        "AI Model",
                        available_models,
                        format_func=lambda x: model_names.get(x, x),
                        help="Choose the AI model for analysis"
                    )
                    models_to_use = [selected_model]
                else:
                    # Multiple model selection
                    selected_models = st.multiselect(
                        "AI Models to Compare",
                        available_models,
                        default=available_models[:min(2, len(available_models))],
                        format_func=lambda x: model_names.get(x, x),
                        help="Select 2-4 models to compare"
                    )
                    
                    if len(selected_models) < 2:
                        st.warning("⚠️ Select at least 2 models for comparison")
                        models_to_use = []
                    else:
                        models_to_use = selected_models
                
                # Show API key status
                st.divider()
                st.caption("**API Keys Configured:**")
                if os.getenv("GEMINI_API_KEY"):
                    st.caption("✅ Google Gemini")
                if os.getenv("OPENAI_API_KEY"):
                    st.caption("✅ OpenAI")
                if os.getenv("ANTHROPIC_API_KEY"):
                    st.caption("✅ Anthropic Claude")
                
                # Analysis options
                st.divider()
                st.subheader("Analysis Options")
                analysis_depth = st.selectbox(
                    "Analysis Depth",
                    ["Quick", "Comprehensive", "Focused"],
                    help="Quick: Fast overview\nComprehensive: Full analysis\nFocused: Specific areas"
                )
                
                focus_areas = st.multiselect(
                    "Focus Areas (Optional)",
                    ["Contract Terms", "Compliance", "Liability", "Intellectual Property", 
                     "Employment Law", "Privacy & Data Protection", "Financial Terms", "Dispute Resolution"],
                    help="Select specific areas to focus the analysis on"
                )
                
                # Analyze button
                if models_to_use:
                    if st.button("🔍 Analyze Document", type="primary"):
                        if analysis_mode == "single":
                            analyze_document(uploaded_file, processor, models_to_use[0], analysis_depth, focus_areas)
                        else:
                            compare_models(uploaded_file, processor, models_to_use, analysis_depth, focus_areas)
    
    # Main content area
    if st.session_state.analysis_mode == "compare" and st.session_state.comparison_results:
        display_comparison_results()
    elif st.session_state.analysis_results is not None:
        display_analysis_results(report_gen)
    else:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### Welcome to LegalMind
            
            Upload a legal document to get started with AI-powered analysis:
            
            - **🤖 Multi-Model Support** - Choose from Gemini, GPT-4, or Claude
            - **📊 Model Comparison** - Compare results from multiple AI models
            - **📈 Accuracy Scoring** - See performance metrics and confidence levels
            - **⚖️ Legal Issue Detection** - Identify risks and compliance gaps
            - **💡 Actionable Insights** - Get specific recommendations
            
            **Supported Formats:** PDF, Word Documents (.docx), Text Files (.txt)
            
            ---
            
            **Setup:**
            Add API keys to your .env file:
            - `GEMINI_API_KEY` (free tier available)
            - `OPENAI_API_KEY` (optional)
            - `ANTHROPIC_API_KEY` (optional)
            """)

def analyze_document(uploaded_file, processor, model_name, analysis_depth, focus_areas):
    """Process and analyze the uploaded document with a single model"""
    
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
    
    with st.spinner(f"Analyzing with {LegalAnalyzer.AVAILABLE_MODELS.get(model_name, {}).get('name', model_name)}..."):
        try:
            # Create analyzer with selected model
            analyzer = LegalAnalyzer(model_name=model_name)
            
            # Perform legal analysis
            analysis_results = analyzer.analyze_document(
                text_content, 
                analysis_depth, 
                focus_areas,
                uploaded_file.name
            )
            
            # Store results
            st.session_state.analysis_results = analysis_results
            st.session_state.comparison_results = None  # Clear comparison results
            
            st.success("✅ Analysis completed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

def compare_models(uploaded_file, processor, models, analysis_depth, focus_areas):
    """Compare analysis results from multiple models"""
    
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
    
    # Run comparison
    try:
        comparison_results = ModelComparator.compare_models(
            text_content,
            models,
            analysis_depth,
            focus_areas,
            uploaded_file.name
        )
        
        # Store results
        st.session_state.comparison_results = comparison_results
        st.session_state.analysis_results = None  # Clear single analysis results
        
        st.success("✅ Model comparison completed!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error during comparison: {str(e)}")

def display_comparison_results():
    """Display comparison results from multiple models"""
    
    results = st.session_state.comparison_results
    individual_results = results.get('individual_results', {})
    comparison_metrics = results.get('comparison_metrics', {})
    
    st.header("🔬 Multi-Model Comparison Results")
    st.markdown(f"**Document:** {st.session_state.filename}")
    st.markdown(f"**Models Compared:** {comparison_metrics.get('models_compared', 0)}")
    
    # Tabs for different views
    tabs = st.tabs(["📊 Accuracy Scores", "⚖️ Consensus Issues", "⚡ Performance", "📋 Individual Results"])
    
    # Tab 1: Accuracy Scores
    with tabs[0]:
        st.subheader("Model Accuracy Scores")
        st.markdown("*Scores based on confidence levels, issue detection, and risk assessment consistency*")
        
        accuracy_scores = comparison_metrics.get('accuracy_scores', {})
        
        if accuracy_scores:
            # Create DataFrame for display
            df_accuracy = pd.DataFrame([
                {
                    'Model': LegalAnalyzer.AVAILABLE_MODELS.get(model, {}).get('name', model),
                    'Accuracy Score': score,
                    'Model ID': model
                }
                for model, score in accuracy_scores.items()
            ]).sort_values('Accuracy Score', ascending=False)
            
            # Display bar chart
            fig = px.bar(
                df_accuracy,
                x='Model',
                y='Accuracy Score',
                title="Model Accuracy Comparison",
                color='Accuracy Score',
                color_continuous_scale='Viridis',
                text='Accuracy Score'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(showlegend=False, yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)
            
            # Display table
            st.dataframe(df_accuracy[['Model', 'Accuracy Score']], hide_index=True, use_container_width=True)
            
            # Winner
            best_model = df_accuracy.iloc[0]
            st.success(f"🏆 **Best Performing Model:** {best_model['Model']} ({best_model['Accuracy Score']:.1f}%)")
    
    # Tab 2: Consensus Issues
    with tabs[1]:
        st.subheader("Issues Identified by Multiple Models")
        st.markdown("*Issues that multiple AI models agree on*")
        
        consensus_issues = comparison_metrics.get('consensus_issues', [])
        
        if consensus_issues:
            for issue in consensus_issues[:10]:  # Top 10
                with st.expander(f"**{issue['category']}** - {issue['risk_level']} Risk (Found by {issue['count']} models)"):
                    st.markdown(f"**Models in agreement:** {', '.join([LegalAnalyzer.AVAILABLE_MODELS.get(m, {}).get('name', m) for m in issue['models']])}")
        else:
            st.info("No consensus issues found. Models identified different concerns.")
    
    # Tab 3: Performance Metrics
    with tabs[2]:
        st.subheader("Performance Comparison")
        
        performance = comparison_metrics.get('performance_comparison', {})
        
        if performance:
            # Create comparison DataFrame
            perf_data = []
            for model, metrics in performance.items():
                perf_data.append({
                    'Model': LegalAnalyzer.AVAILABLE_MODELS.get(model, {}).get('name', model),
                    'Response Time (s)': metrics.get('response_time', 0),
                    'Tokens Used': metrics.get('tokens_used', 0),
                    'Issues Found': metrics.get('issues_found', 0),
                    'Avg Confidence': metrics.get('avg_confidence', 0)
                })
            
            df_perf = pd.DataFrame(perf_data)
            
            # Display metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Response time chart
                fig_time = px.bar(
                    df_perf,
                    x='Model',
                    y='Response Time (s)',
                    title="Response Time Comparison",
                    color='Response Time (s)',
                    color_continuous_scale='RdYlGn_r'
                )
                st.plotly_chart(fig_time, use_container_width=True)
                
                # Issues found chart
                fig_issues = px.bar(
                    df_perf,
                    x='Model',
                    y='Issues Found',
                    title="Issues Detected",
                    color='Issues Found',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_issues, use_container_width=True)
            
            with col2:
                # Tokens used chart
                fig_tokens = px.bar(
                    df_perf,
                    x='Model',
                    y='Tokens Used',
                    title="Token Usage",
                    color='Tokens Used',
                    color_continuous_scale='Oranges'
                )
                st.plotly_chart(fig_tokens, use_container_width=True)
                
                # Confidence chart
                fig_conf = px.bar(
                    df_perf,
                    x='Model',
                    y='Avg Confidence',
                    title="Average Confidence",
                    color='Avg Confidence',
                    color_continuous_scale='Greens'
                )
                fig_conf.update_layout(yaxis_range=[0, 1])
                st.plotly_chart(fig_conf, use_container_width=True)
            
            # Performance summary table
            st.dataframe(df_perf, hide_index=True, use_container_width=True)
    
    # Tab 4: Individual Results
    with tabs[3]:
        st.subheader("Individual Model Results")
        
        for model, result in individual_results.items():
            model_name = LegalAnalyzer.AVAILABLE_MODELS.get(model, {}).get('name', model)
            
            with st.expander(f"**{model_name}** Results"):
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Risk Score", f"{result.get('overall_risk_score', 0):.1f}/10")
                    col2.metric("Issues Found", result.get('performance_metrics', {}).get('issues_found', 0))
                    col3.metric("Avg Confidence", f"{result.get('performance_metrics', {}).get('confidence_avg', 0):.2f}")
                    col4.metric("Response Time", f"{result.get('performance_metrics', {}).get('response_time', 0):.2f}s")
                    
                    # Issues list
                    st.markdown("**Issues Identified:**")
                    for i, issue in enumerate(result.get('issues', [])[:5], 1):  # Top 5 issues
                        st.markdown(f"{i}. **{issue.get('title')}** ({issue.get('risk_level')} Risk, {issue.get('confidence', 0):.0%} confidence)")
                        st.caption(issue.get('description', '')[:200] + "...")

def display_analysis_results(report_gen):
    """Display single model analysis results"""
    
    results = st.session_state.analysis_results
    metadata = results.get('analysis_metadata', {})
    performance = results.get('performance_metrics', {})
    
    # Header
    st.header("📊 Analysis Results")
    st.markdown(f"**Document:** {metadata.get('filename', 'Unknown')}")
    st.markdown(f"**Model:** {LegalAnalyzer.AVAILABLE_MODELS.get(metadata.get('model_used', ''), {}).get('name', metadata.get('model_used', 'Unknown'))}")
    st.markdown(f"**Analysis Time:** {performance.get('response_time', 0):.2f}s")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Risk Score", f"{results.get('overall_risk_score', 0):.1f}/10")
    col2.metric("Issues Found", performance.get('issues_found', 0))
    col3.metric("Avg Confidence", f"{performance.get('confidence_avg', 0):.1%}")
    col4.metric("Tokens Used", performance.get('tokens_used', 0))
    
    # Rest of the analysis display (executive summary, issues, etc.)
    st.divider()
    
    # Executive Summary
    st.subheader("Executive Summary")
    st.write(results.get('executive_summary', 'No summary available'))
    
    # Key Findings
    with st.expander("🔑 Key Findings", expanded=True):
        for finding in results.get('key_findings', []):
            st.markdown(f"• {finding}")
    
    # Issues
    st.subheader("Identified Issues")
    issues = results.get('issues', [])
    
    for i, issue in enumerate(issues, 1):
        risk_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(issue.get('risk_level', 'Medium'), "⚪")
        
        with st.expander(f"{risk_color} **Issue {i}: {issue.get('title')}** ({issue.get('confidence', 0):.0%} confidence)"):
            st.markdown(f"**Category:** {issue.get('category')}")
            st.markdown(f"**Risk Level:** {issue.get('risk_level')}")
            st.markdown(f"**Description:** {issue.get('description')}")
            st.markdown(f"**Impact:** {issue.get('potential_impact')}")
            
            st.markdown("**Recommendations:**")
            for rec in issue.get('recommendations', []):
                st.markdown(f"• {rec}")

if __name__ == "__main__":
    main()
