from .rules import validate_schedule, validate_budget, SEV_ERROR

def evaluate_itinerary(trip, itinerary_data):
    errors = []
    warnings = []
    
    # Run all rules
    s_errors, s_warnings = validate_schedule(trip, itinerary_data)
    errors.extend(s_errors)
    warnings.extend(s_warnings)
    
    b_errors, b_warnings = validate_budget(trip, itinerary_data)
    errors.extend(b_errors)
    warnings.extend(b_warnings)
    
    # Deterministic scoring
    # 100 - (errors * 20) - (warnings * 5)
    # Ensure errors are only those with SEV_ERROR
    error_count = len([e for e in errors if e.get('severity') == SEV_ERROR])
    warning_count = len([w for w in warnings if w.get('severity') != SEV_ERROR] + 
                        [e for e in errors if e.get('severity') != SEV_ERROR])
    
    score = 100 - (error_count * 20) - (warning_count * 5)
    score = max(0, min(100, score))
    
    # Quality Gates
    status = "PASS"
    if error_count > 0:
        status = "FAIL"
    elif warning_count > 0 and score < 75:
        status = "WARNING"
        
    return {
        "score": score,
        "status": status,
        "warnings": warnings,
        "errors": errors,
        "metrics": {"total_errors": len(errors), "total_warnings": len(warnings)},
        "version": "1.0"
    }
