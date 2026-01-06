import streamlit as st
from typing import Dict, Any

def validate_file(uploaded_file) -> Dict[str, Any]:
    """
    Validate uploaded file for security and format compliance
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Dictionary with validation results
    """
    
    # File size validation (200MB limit)
    max_size = 200 * 1024 * 1024  # 200MB in bytes
    
    if uploaded_file.size > max_size:
        return {
            'valid': False,
            'message': f"File size ({uploaded_file.size / (1024*1024):.1f}MB) exceeds maximum allowed size (200MB)."
        }
    
    # File type validation
    allowed_types = {
        'application/pdf': ['.pdf'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'text/plain': ['.txt']
    }
    
    file_extension = '.' + uploaded_file.name.split('.')[-1].lower()
    
    if uploaded_file.type not in allowed_types:
        return {
            'valid': False,
            'message': f"File type '{uploaded_file.type}' is not supported. Please upload PDF, DOCX, or TXT files."
        }
    
    if file_extension not in allowed_types[uploaded_file.type]:
        return {
            'valid': False,
            'message': f"File extension '{file_extension}' does not match the detected file type."
        }
    
    # File name validation
    if len(uploaded_file.name) > 255:
        return {
            'valid': False,
            'message': "Filename is too long (maximum 255 characters)."
        }
    
    # Check for suspicious file names
    suspicious_patterns = ['..', '/', '\\', '<script', 'javascript:', 'data:']
    filename_lower = uploaded_file.name.lower()
    
    for pattern in suspicious_patterns:
        if pattern in filename_lower:
            return {
                'valid': False,
                'message': "Filename contains potentially unsafe characters."
            }
    
    # Basic content validation
    if uploaded_file.size < 10:  # Very small files are likely empty or corrupted
        return {
            'valid': False,
            'message': "File appears to be empty or corrupted."
        }
    
    return {
        'valid': True,
        'message': "File validation successful."
    }

def format_confidence_score(confidence: float) -> str:
    """
    Format confidence score for display
    
    Args:
        confidence: Confidence score between 0 and 1
        
    Returns:
        Formatted confidence string
    """
    percentage = confidence * 100
    
    if percentage >= 90:
        return f"🟢 {percentage:.1f}% (Very High)"
    elif percentage >= 70:
        return f"🟡 {percentage:.1f}% (High)"
    elif percentage >= 50:
        return f"🟠 {percentage:.1f}% (Medium)"
    else:
        return f"🔴 {percentage:.1f}% (Low)"

def format_risk_level(risk_level: str) -> str:
    """
    Format risk level with appropriate emoji
    
    Args:
        risk_level: Risk level string
        
    Returns:
        Formatted risk level string
    """
    risk_map = {
        'high': '🔴 High Risk',
        'medium': '🟡 Medium Risk',
        'low': '🟢 Low Risk'
    }
    
    return risk_map.get(risk_level.lower(), f"⚪ {risk_level.title()} Risk")

def sanitize_text_input(text: str) -> str:
    """
    Basic text sanitization for security
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous HTML/script tags
    dangerous_patterns = [
        '<script', '</script>',
        '<iframe', '</iframe>',
        'javascript:',
        'data:text/html',
        'vbscript:',
        'onload=',
        'onerror='
    ]
    
    sanitized = text
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern, '')
    
    return sanitized.strip()

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def get_file_icon(file_type: str) -> str:
    """
    Get appropriate icon for file type
    
    Args:
        file_type: MIME type of the file
        
    Returns:
        Emoji icon for the file type
    """
    icon_map = {
        'application/pdf': '📄',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '📝',
        'text/plain': '📃'
    }
    
    return icon_map.get(file_type, '📄')

def calculate_reading_time(text: str) -> str:
    """
    Calculate estimated reading time for text
    
    Args:
        text: Text content
        
    Returns:
        Formatted reading time estimate
    """
    # Average reading speed: 200-250 words per minute
    words = len(text.split())
    minutes = words / 225  # Using 225 WPM as average
    
    if minutes < 1:
        return "< 1 minute"
    elif minutes < 60:
        return f"{minutes:.0f} minutes"
    else:
        hours = minutes / 60
        return f"{hours:.1f} hours"

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
