import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Prompt Template
# -----------------------------
PROMPT_TEMPLATE = """
You are an insurance claims analyst. You will evaluate the following claim note.

Claim Note:
\"\"\"{claim_text}\"\"\"

Your tasks:

1. **Clarity Score (1–5)**  
Evaluate how clearly the note is written.  
- 1 = very unclear  
- 3 = somewhat clear  
- 5 = very clear  
Provide:  
- Clarity Score  
- One-sentence reason

2. **Complexity Score (1–5)**  
Evaluate how complex the incident is.  
- 1 = simple (single vehicle, no injuries, clear liability)  
- 3 = moderate  
- 5 = complex (multiple parties, injuries, disputes)  
Provide:  
- Complexity Score  
- One-sentence reason

3. **Contributing Factors**  
Extract a **list of key contributing factors** from the note.  
Examples: speeding, weather, fatigue, following distance, distraction, cargo load, mechanical failure, road condition.

Rules:
1. DO NOT infer or guess any contributing factors.
2. DO NOT label anything as a contributing factor if it is described as a POST-ACCIDENT change, symptom, or new condition.
3. If the note does not explicitly state a pre-accident condition (e.g., fatigue, distraction, impairment, etc.), DO NOT label it.
4. Only return factors that are clearly and directly mentioned as contributing causes before the accident.
5. If no valid pre-accident contributing factor is explicitly stated, return an empty array [].

IMPORTANT: Return ONLY valid JSON. Do not include any markdown formatting, code blocks, or explanatory text.

Return results in this exact JSON format:
{{
  "clarity_score": <number 1-5>,
  "clarity_reason": "<string>",
  "complexity_score": <number 1-5>,
  "complexity_reason": "<string>",
  "contributing_factors": [<array of strings>]
}}
"""

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Claim Note Scoring App", layout="wide")
st.title("🚗 Insurance Claim LLM Scoring App")
st.write("Enter a claim note below and the model will evaluate clarity, complexity, and contributing factors.")

# Text input box
claim_text = st.text_area("Claim Note", height=200, placeholder="Paste a claim note here...")

# Run button
if st.button("Score Claim", type="primary"):

    if not claim_text.strip():
        st.error("Please enter a claim note.")
        st.stop()

    with st.spinner("Scoring claim..."):
        prompt = PROMPT_TEMPLATE.format(claim_text=claim_text)

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a highly reliable insurance claims evaluation assistant. You always return valid JSON without any markdown formatting or code blocks."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                response_format={"type": "json_object"}
            )

            raw_output = completion.choices[0].message.content
            
            # Clean up the output in case it has markdown code blocks
            raw_output = raw_output.strip()
            if raw_output.startswith("```json"):
                raw_output = raw_output[7:]
            if raw_output.startswith("```"):
                raw_output = raw_output[3:]
            if raw_output.endswith("```"):
                raw_output = raw_output[:-3]
            raw_output = raw_output.strip()
            
            # Parse JSON result
            parsed = json.loads(raw_output)
            
            # Normalize the result - handle nested objects and strip whitespace from all keys
            def normalize_keys(obj):
                if isinstance(obj, dict):
                    return {k.strip(): normalize_keys(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [normalize_keys(item) for item in obj]
                else:
                    return obj
            
            result = normalize_keys(parsed)

        except json.JSONDecodeError as je:
            st.error(f"Model returned invalid JSON. Error: {je}")
            st.code(raw_output, language="text")
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            with st.expander("Debug Info"):
                st.write("Raw output:")
                st.code(raw_output, language="text")
                if 'parsed' in locals():
                    st.write("Parsed result:")
                    st.json(parsed)
                    st.write("Keys in result:")
                    st.write(list(parsed.keys()))
            st.stop()

        # Display results
        st.subheader("📊 Results")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Clarity Score")
            st.metric("Score", result.get("clarity_score", "N/A"))
            st.write(result.get("clarity_reason", ""))

        with col2:
            st.markdown("### Complexity Score")
            st.metric("Score", result.get("complexity_score", "N/A"))
            st.write(result.get("complexity_reason", ""))

        st.markdown("### 🧩 Contributing Factors")
        factors = result.get("contributing_factors", [])
        if factors == "None" or factors == []:
            st.info("No contributing factors explicitly stated.")
        else:
            for f in factors:
                st.success(f"- {f}")

        st.markdown("### 🔍 Raw Model Output (Debug)")
        st.code(raw_output, language="json")
