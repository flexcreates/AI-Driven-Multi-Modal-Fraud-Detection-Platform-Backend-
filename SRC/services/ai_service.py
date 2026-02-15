import asyncio
import random

async def analyze_text(content: str) -> dict:
    await asyncio.sleep(1.5) # Simulate processing
    # Mocking logic
    fraud_prob = random.uniform(0.0, 1.0)
    return {"fraud_probability": fraud_prob, "sentiment": "negative" if fraud_prob > 0.6 else "neutral"}

async def analyze_url(url: str) -> dict:
    await asyncio.sleep(1.0)
    phishing_prob = random.uniform(0.0, 1.0)
    return {"phishing_probability": phishing_prob, "domain_age": "1 month"}

async def analyze_file(filename: str, file_content: bytes) -> dict:
    await asyncio.sleep(2.0)
    malware_prob = random.uniform(0.0, 1.0)
    return {"malware_probability": malware_prob, "file_type": filename.split('.')[-1]}
