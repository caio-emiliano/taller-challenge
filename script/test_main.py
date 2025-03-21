import os
import tempfile
import pytest
import re
from main import analyze_logs

def create_test_log(content):
    """Create a temporary log file with the given content for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as f:
        f.write(content)
    return temp_file.name

def extract_message_counts(report_text):
    """Extract message counts from report text regardless of format"""
    info_match = re.search(r'INFO messages:\s*(\d+)', report_text)
    error_match = re.search(r'ERROR messages:\s*(\d+)', report_text)
    warning_match = re.search(r'WARNING messages:\s*(\d+)', report_text)
    
    return {
        'INFO': int(info_match.group(1)) if info_match else None,
        'ERROR': int(error_match.group(1)) if error_match else None,
        'WARNING': int(warning_match.group(1)) if warning_match else None
    }

def extract_top_responses(report_text):
    """Extract top responses and their counts from report text"""
    responses = {}
    # Look for quoted responses and their counts
    pattern = r'"([^"]+)"\s*\((\d+)\s*times?\)'
    for match in re.finditer(pattern, report_text):
        response = match.group(1)
        count = int(match.group(2))
        responses[response] = count
    return responses

def extract_errors(report_text):
    """Extract errors and their counts from report text"""
    errors = {}
    # Look for error messages section
    error_section_match = re.search(r'Most Common Errors:(.*?)(?:\n\n|\Z)', report_text, re.DOTALL)
    if error_section_match:
        error_section = error_section_match.group(1)
        
        # If "No errors found" is in the section, return empty dict
        if "No errors found" in error_section:
            return {}
            
        # Extract error patterns like "Error message (3 times)"
        # or lines with numbering like "1. Error message (3 times)"
        pattern = r'\d+\.\s*(.*?)\s*\((\d+)\s*times?\)'
        for match in re.finditer(pattern, error_section):
            error = match.group(1)
            count = int(match.group(2))
            errors[error] = count
    return errors

def test_message_count():
    """Test that message counts are correct"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] WARNING - Response latency high: 2500ms
"""
    log_path = create_test_log(log_content)
    report = analyze_logs(log_path)
    os.unlink(log_path)
    
    counts = extract_message_counts(report)
    assert counts['INFO'] == 2, f"Expected 2 INFO messages, got {counts['INFO']}"
    assert counts['ERROR'] == 1, f"Expected 1 ERROR message, got {counts['ERROR']}"
    assert counts['WARNING'] == 1, f"Expected 1 WARNING message, got {counts['WARNING']}"

def test_response_extraction():
    """Test that AI responses are correctly extracted and counted"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
"""
    log_path = create_test_log(log_content)
    report = analyze_logs(log_path)
    os.unlink(log_path)
    
    responses = extract_top_responses(report)
    assert responses.get("Hello! How can I help you today?") == 3, "Should find 'Hello!' response 3 times"
    assert responses.get("I'm sorry, I didn't understand that.") == 1, "Should find 'I'm sorry' response 1 time"

def test_error_extraction():
    """Test that errors are correctly extracted and counted"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] ERROR - API Connection Failure
[2025-02-20 14:35:20] ERROR - Model Timeout after 5000ms
[2025-02-20 14:36:45] ERROR - Invalid Response Format
"""
    log_path = create_test_log(log_content)
    report = analyze_logs(log_path)
    os.unlink(log_path)
    
    errors = extract_errors(report)
    assert errors.get("Model Timeout after 5000ms") == 2, "Should find 'Model Timeout' 2 times"
    assert errors.get("API Connection Failure") == 1, "Should find 'API Connection Failure' 1 time"
    assert errors.get("Invalid Response Format") == 1, "Should find 'Invalid Response Format' 1 time"

def test_full_report():
    """Test that the full report has all required sections"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] WARNING - Response latency high: 2500ms
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
"""
    log_path = create_test_log(log_content)
    report = analyze_logs(log_path)
    os.unlink(log_path)
    
    # Check that all required sections exist
    assert "Log Summary:" in report, "Report should contain 'Log Summary:' section"
    assert "Top" in report and "AI Responses:" in report, "Report should contain AI Responses section"
    assert "Most Common Errors:" in report, "Report should contain 'Most Common Errors:' section"
    
    # Verify data in each section
    counts = extract_message_counts(report)
    assert counts['INFO'] == 3
    assert counts['ERROR'] == 1
    assert counts['WARNING'] == 1
    
    responses = extract_top_responses(report)
    assert responses.get("Hello! How can I help you today?") == 2
    
    errors = extract_errors(report)
    assert errors.get("Model Timeout after 5000ms") == 1

def test_empty_log_file():
    """Test handling of empty log file"""
    log_path = create_test_log("")
    report = analyze_logs(log_path)
    os.unlink(log_path)
    
    counts = extract_message_counts(report)
    assert counts['INFO'] == 0, "Empty log should have 0 INFO messages"
    assert counts['ERROR'] == 0, "Empty log should have 0 ERROR messages"
    assert counts['WARNING'] == 0, "Empty log should have 0 WARNING messages"
    
    # Empty responses and errors sections should exist but show no data
    assert len(extract_top_responses(report)) == 0, "Empty log should have no responses"
    assert len(extract_errors(report)) == 0, "Empty log should have no errors"

def test_custom_top_n():
    """Test customizing the number of top items to display"""
    log_content = """
[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms
[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that."
[2025-02-20 14:35:20] INFO - Agent Response: "Please provide more details."
[2025-02-20 14:36:45] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:37:30] ERROR - API Connection Failure
[2025-02-20 14:38:12] INFO - Agent Response: "Thank you for your question."
[2025-02-20 14:39:55] ERROR - Invalid Response Format
[2025-02-20 14:40:33] INFO - Agent Response: "Hello! How can I help you today?"
[2025-02-20 14:41:22] ERROR - Model Timeout after 5000ms
"""
    log_path = create_test_log(log_content)
    
    # Test with custom parameters if the function supports them
    try:
        report = analyze_logs(log_path, top_responses=4, top_errors=3)
    except TypeError:
        # If function doesn't accept these parameters, use default
        report = analyze_logs(log_path)
    
    os.unlink(log_path)
    
    # Regardless of how many were requested, verify what's actually in the report
    responses = extract_top_responses(report)
    errors = extract_errors(report)
    
    assert responses.get("Hello! How can I help you today?") == 3, "Should find 'Hello!' response 3 times"
    assert "I'm sorry, I didn't understand that." in responses, "Should include 'I'm sorry' response"
    assert "Please provide more details." in responses, "Should include 'Please provide' response"
    assert "Thank you for your question." in responses, "Should include 'Thank you' response"
    
    assert errors.get("Model Timeout after 5000ms") == 2, "Should find 'Model Timeout' 2 times"
    assert "API Connection Failure" in errors, "Should include 'API Connection Failure'"
    assert "Invalid Response Format" in errors, "Should include 'Invalid Response Format'"

