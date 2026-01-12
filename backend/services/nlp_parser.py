import re

def parse_medicine_text(text: str):
    name_match = re.search(r"(paracetamol|ibuprofen|aspirin)", text, re.I)
    dosage_match = re.search(r"\d+mg", text)
    time_match = re.search(r"\b\d{1,2}:\d{2}\b", text)
    freq_match = re.search(r"(daily|every day|weekly)", text, re.I)

    if not name_match:
        raise ValueError("Medicine name missing")

    return {
        "name": name_match.group(0).capitalize(),
        "dosage": dosage_match.group(0) if dosage_match else "unknown",
        "time": time_match.group(0) if time_match else "09:00",
        "frequency": freq_match.group(0).lower() if freq_match else "daily"
    }
