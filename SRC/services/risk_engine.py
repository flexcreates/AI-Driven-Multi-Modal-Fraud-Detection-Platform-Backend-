from SRC.logs.logger import get_logger

logger = get_logger("services.risk")


def calculate_risk_score(ai_results: dict, input_type: str) -> dict:
    """
    Calculate the final risk score, level, and decision based on AI analysis results.
    
    Risk Levels:
        - HIGH   (>0.8): BLOCK — Confirmed fraudulent/malicious
        - MEDIUM (>0.4): FLAG  — Suspicious, needs review
        - LOW    (<=0.4): ALLOW — Appears safe
    
    Args:
        ai_results: Dictionary of scores from the AI service.
        input_type: One of TEXT, URL, DOCUMENT, IMAGE, FILE.
    
    Returns:
        dict with risk_score, risk_level, and decision.
    """
    risk_score = 0.0

    if input_type == "TEXT":
        risk_score = ai_results.get("fraud_probability", 0.0)
    elif input_type == "URL":
        risk_score = ai_results.get("phishing_probability", 0.0)
    elif input_type in ("DOCUMENT", "FILE"):
        risk_score = ai_results.get("malware_probability", 0.0)
    elif input_type == "IMAGE":
        # Weighted: 60% metadata suspicion + 40% steganography
        metadata = ai_results.get("metadata_suspicion", 0.0)
        stego = ai_results.get("steganography_score", 0.0)
        risk_score = (0.6 * metadata) + (0.4 * stego)

    risk_score = round(min(max(risk_score, 0.0), 1.0), 4)  # Clamp to [0, 1]

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

    logger.info(
        f"Risk calculated for {input_type}: "
        f"score={risk_score}, level={level}, decision={decision}"
    )

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "decision": decision,
    }
