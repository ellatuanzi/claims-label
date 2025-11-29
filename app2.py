import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =====================================================
# Prompt Template (Full)
# =====================================================
PROMPT_TEMPLATE = """
You are an insurance claims analyst. You will evaluate the following claim note.

Claim Note:
\"\"\"{claim_text}\"\"\"


Your tasks:

------------------------------------------------------------
1. **Clarity Score (1–5)**  
- 1 = very unclear  
- 3 = somewhat clear  
- 5 = very clear  
Return:
- clarity_score  
- clarity_reason  

------------------------------------------------------------
2. **Complexity Score (1–5)**  
- 1 = simple  
- 3 = moderate  
- 5 = complex  
Return:
- complexity_score  
- complexity_reason  

------------------------------------------------------------
3. **Contributing Factors**  
Extract explicit pre-accident contributing factors only.
Rules:
- Do NOT infer or guess.
- Do NOT use post-accident conditions.
- If none explicitly stated, return ["None"].

Return:
- contributing_factors: list

------------------------------------------------------------
4. **Inconsistency Detection**  
Identify contradictions or conflicting statements in the narrative.

Examples:
- "driver uninjured" vs later "reports neck pain"
- single-vehicle vs describes another vehicle
- time mismatch
- location mismatch
- police report inconsistencies

Return:
- inconsistencies: list of strings  
If none: return ["None"]

------------------------------------------------------------
5. **Structured Information Extraction**  
Extract structured fields ONLY if explicitly mentioned.

Return JSON object:
extracted_info = {{{{
    "incident_date": "...",
    "location": "...",
    "vehicles_involved": "...",
    "injuries": "...",
    "weather": "...",
    "road_condition": "...",
    "speed": "...",
    "police_report": "...",
    "liability_statement": "...",
    "citation": "...",
    "cargo_load": "...",
    "distraction": "...",
    "mechanical_issue": "...",
}}}}

If a field does not appear, use null.

------------------------------------------------------------

Return a JSON with keys:
{{
 "clarity_score": int,
 "clarity_reason": str,
 "complexity_score": int,
 "complexity_reason": str,
 "contributing_factors": list,
 "inconsistencies": list,
 "extracted_info": dict
}}
"""

# =====================================================
# OpenAI Function
# =====================================================
def score_claim(claim_text: str):
    prompt = PROMPT_TEMPLATE.format(claim_text=claim_text)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a highly reliable insurance claims evaluation assistant. Return ONLY valid JSON without any markdown formatting."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        raw = completion.choices[0].message.content
        
        # Clean up any markdown formatting
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
        
        parsed = json.loads(raw)
        
        # Normalize keys - strip whitespace and newlines from all keys
        def normalize_keys(obj):
            if isinstance(obj, dict):
                return {k.strip(): normalize_keys(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [normalize_keys(item) for item in obj]
            else:
                return obj
        
        result = normalize_keys(parsed)
        return result
        
    except Exception as e:
        st.error(f"Error scoring claim: {e}")
        if 'raw' in locals():
            st.write("Raw output:")
            st.code(raw, language="text")
        raise


# =====================================================
# Streamlit Interface
# =====================================================

st.title("📄 Advanced Claim Analysis App (LLM-Powered)")
st.write("Scoring • Contributing Factors • Inconsistency Detection • Information Extraction • Batch Analytics")

mode = st.sidebar.radio(
    "Select Mode",
    ["Single Claim Analysis", "Batch Folder Analysis"]
)


# =====================================================
# Mode 1 — Single Claim
# =====================================================
if mode == "Single Claim Analysis":
    st.header("🔍 Analyze a Single Claim")

    claim_text = st.text_area("Enter claim note:", height=200)

    if st.button("Run Analysis"):
        if not claim_text.strip():
            st.error("Please enter claim text.")
        else:
            result = score_claim(claim_text)
            
            # Debug: show what keys are in the result
            st.write("DEBUG - Keys in result:", list(result.keys()))

            st.subheader("⭐ Clarity & Complexity Scores")
            st.write(f"**Clarity:** {result.get('clarity_score', 'N/A')} — {result.get('clarity_reason', '')}")
            st.write(f"**Complexity:** {result.get('complexity_score', 'N/A')} — {result.get('complexity_reason', '')}")

            st.subheader("🔍 Contributing Factors")
            st.json(result.get("contributing_factors", []))

            st.subheader("⚠ Inconsistencies")
            st.json(result.get("inconsistencies", []))

            st.subheader("📋 Extracted Structured Info")
            st.json(result.get("extracted_info", {}))
            
            st.subheader("🔧 Raw Result (Debug)")
            st.json(result)


# =====================================================
# Mode 2 — Batch
# =====================================================
if mode == "Batch Folder Analysis":
    st.header("📂 Batch Analysis from JSON Files")

    uploaded_files = st.file_uploader(
        "Upload claim JSON files (each must contain 'claim_text')",
        type=["json"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} files uploaded.")

        records = []
        factor_counts = {}
        inconsistency_counts = {}

        for file in uploaded_files:
            data = json.load(file)
            
            # Handle both single object and array of objects
            items = data if isinstance(data, list) else [data]
            
            for item in items:
                # Try both 'claim_note' and 'claim_text' keys
                text = item.get("claim_note", item.get("claim_text", ""))
                
                if not text.strip():
                    continue
                    
                result = score_claim(text)
                result["claim_text"] = text
                records.append(result)

                # Count contributing factors
                for f in result["contributing_factors"]:
                    if f not in ["None", "", None]:
                        factor_counts[f] = factor_counts.get(f, 0) + 1

                # Count inconsistencies
                for inc in result["inconsistencies"]:
                    if inc not in ["None", "", None]:
                        inconsistency_counts[inc] = inconsistency_counts.get(inc, 0) + 1

        # Aggregates
        avg_clarity = sum(r["clarity_score"] for r in records) / len(records)
        avg_complexity = sum(r["complexity_score"] for r in records) / len(records)

        st.subheader("📊 Aggregate Scores")
        st.write(f"**Average Clarity:** {avg_clarity:.2f}")
        st.write(f"**Average Complexity:** {avg_complexity:.2f}")

        st.subheader("🔥 Contributing Factor Distribution")
        st.json(factor_counts)

        st.subheader("⚠ Inconsistency Frequency")
        st.json(inconsistency_counts)

        st.subheader("📄 Sample Extracted Info (first item)")
        st.json(records[0]["extracted_info"])
