def calculate_risk_score(ai_results: dict, input_type: str) -> dict:
    risk_score = 0.0
    
    if input_type == "TEXT":
        risk_score = ai_results.get("fraud_probability", 0.0)
    elif input_type == "URL":
        risk_score = ai_results.get("phishing_probability", 0.0)
    elif input_type in ["DOCUMENT", "IMAGE", "FILE"]:
        risk_score = ai_results.get("malware_probability", 0.0)
        
    # Determine Level and Decision
    if risk_score > 0.8:
        level = "HIGH"
        decision = "BLOCK"
    elif risk_score > 0.4:
        level = "MEDIUM"
        decision = "FLAG"
    else:
        level = "LOW"
        decision = "ALLOW"
        
    return {
        "risk_score": risk_score,
        "risk_level": level,
        "decision": decision
    }
