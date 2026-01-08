"""
FastAPI backend wrapper for LegalMind frontend
Run this to expose the Python backend as an API
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import tempfile
import os
from typing import List
import sys

# Add parent directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_processor import DocumentProcessor
from legal_analyzer import LegalAnalyzer, ModelComparator
from report_generator import ReportGenerator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LegalMind API",
    description="AI-powered legal document analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
processor = DocumentProcessor()
report_gen = ReportGenerator()

@app.get("/")
async def root():
    return {
        "name": "LegalMind API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/models")
async def get_models():
    """Get available models"""
    available = LegalAnalyzer.get_available_models()
    return {
        "models": available,
        "model_details": {m: LegalAnalyzer.AVAILABLE_MODELS[m] for m in available}
    }

@app.get("/models/working")
async def get_working_models():
    """Get models that pass a quick health check"""
    working = LegalAnalyzer.get_working_models()
    return {
        "models": working,
        "model_details": {m: LegalAnalyzer.AVAILABLE_MODELS[m] for m in working}
    }

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    analysis_depth: str = Form("Comprehensive"),
    focus_areas: str = Form("[]"),
    model: str = Form("gemini-3-flash-preview")
):
    """Analyze a single document with one model"""
    try:
        # Parse focus areas
        try:
            areas = json.loads(focus_areas)
        except:
            areas = []

        # Read file content
        content = await file.read()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or "")[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Determine MIME type from file extension and extract text
            ext = os.path.splitext(file.filename or "")[1].lower()
            mime_map = {
                ".pdf": "application/pdf",
                ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".txt": "text/plain",
            }
            mime_type = mime_map.get(ext, "text/plain")

            text = processor.extract_text(tmp_path, mime_type)
            if not text:
                return JSONResponse(status_code=400, content={"error": "Could not extract text from the uploaded file."})
            
            # Analyze
            analyzer = LegalAnalyzer(model)
            import time
            start_time = time.time()
            result = analyzer.analyze_document(
                text,
                analysis_depth,
                areas,
                file.filename or "document"
            )
            result['response_time'] = time.time() - start_time
            
            return result
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/compare")
async def compare(
    file: UploadFile = File(...),
    analysis_depth: str = Form("Comprehensive"),
    focus_areas: str = Form("[]"),
    models: str = Form("[]")
):
    """Compare analysis across multiple models"""
    try:
        # Parse inputs
        try:
            areas = json.loads(focus_areas)
        except:
            areas = []
        
        try:
            model_list = json.loads(models)
        except:
            model_list = ["gemini-3-flash-preview"]

        # Read file
        content = await file.read()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or "")[1]) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Determine MIME type from file extension and extract text
            ext = os.path.splitext(file.filename or "")[1].lower()
            mime_map = {
                ".pdf": "application/pdf",
                ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".txt": "text/plain",
            }
            mime_type = mime_map.get(ext, "text/plain")

            text = processor.extract_text(tmp_path, mime_type)
            if not text:
                return JSONResponse(status_code=400, content={"error": "Could not extract text from the uploaded file."})
            
            # Compare
            import time
            start_time = time.time()
            
            # Run analysis with each model
            model_results = []
            for model in model_list:
                try:
                    analyzer = LegalAnalyzer(model)
                    result = analyzer.analyze_document(text, analysis_depth, areas, file.filename or "document")
                    result['model_name'] = model
                    model_results.append(result)
                except Exception as e:
                    # Include error in results but continue with other models
                    model_results.append({
                        'model_name': model,
                        'error': str(e),
                        'issues': [],
                        'overall_risk_score': 0
                    })
            
            comparison_result = {
                'model_results': model_results,
                'response_time': time.time() - start_time
            }
            
            return comparison_result
        finally:
            os.unlink(tmp_path)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
