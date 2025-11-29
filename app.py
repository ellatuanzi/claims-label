import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import altair as alt

# Load API Key
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

1. Clarity Score (1-5): Evaluate how clearly the note is written.
2. Complexity Score (1-5): Evaluate how complex the incident is.
3. Contributing Factors: Extract only the contributing factors that are explicitly mentioned pre-accident.

Rules:
- DO NOT infer or guess.
- If no explicit contributing factor is mentioned, return an empty array [].

IMPORTANT: Return ONLY a valid JSON object with no extra text, markdown, or code blocks.

JSON format (use these exact key names):
{{
  "clarity_score": <number>,
  "clarity_reason": "<string>",
  "complexity_score": <number>,
  "complexity_reason": "<string>",
  "contributing_factors": [<array of strings or empty array>]
}}
"""

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Claim Dataset Analysis", layout="wide")
st.title("📊 Insurance Claim Dataset Analysis (LLM Powered)")

st.write("This tool loads a dataset of claim notes, scores them using an LLM, and generates aggregate analytics.")

# -----------------------------
# Load JSON Dataset
# -----------------------------
DATA_PATH = "synthetic_claim_data.json"

if not os.path.exists(DATA_PATH):
    st.error(f"Dataset not found at {DATA_PATH}.")
    st.stop()

with open(DATA_PATH, "r") as f:
    dataset = json.load(f)

df = pd.DataFrame(dataset)

st.subheader("📄 Loaded Dataset")
st.dataframe(df)

# -----------------------------
# LLM Scoring Function
# -----------------------------
def score_claim(claim_text):
    prompt = PROMPT_TEMPLATE.format(claim_text=claim_text)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a highly reliable insurance claims evaluation assistant. Return ONLY valid JSON without any markdown formatting."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )

        raw_output = completion.choices[0].message.content
        
        # Clean up any markdown formatting
        raw_output = raw_output.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
        raw_output = raw_output.strip()

        parsed = json.loads(raw_output)
        
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
        st.write("Raw output:")
        st.code(raw_output if 'raw_output' in locals() else "No output", language="text")
        raise


# -----------------------------
# Run Scoring
# -----------------------------
if st.button("Run LLM Scoring on Dataset", type="primary"):

    st.info("Running scoring on all claims... This may take 20–40 seconds.")

    results = []
    for idx, row in df.iterrows():
        with st.spinner(f"Scoring claim {row['id']}..."):
            out = score_claim(row["claim_note"])
            out["id"] = row["id"]
            out["claim_note"] = row["claim_note"]
            results.append(out)

    results_df = pd.DataFrame(results)

    st.success("Scoring complete!")

    # Save locally
    results_df.to_json("scored_claims.json", orient="records", indent=2)

    # -----------------------------
    # Analytics
    # -----------------------------
    st.subheader("📈 Dataset Summary Statistics")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Clarity Score", round(results_df["clarity_score"].mean(), 2))
    with col2:
        st.metric("Avg Complexity Score", round(results_df["complexity_score"].mean(), 2))

    # Lowest clarity
    st.subheader("🔍 Claim With Lowest Clarity")
    min_row = results_df.loc[results_df["clarity_score"].idxmin()]
    st.write(min_row["claim_note"])
    st.write(f"Clarity Score: {min_row['clarity_score']} — {min_row['clarity_reason']}")

    # Highest complexity
    st.subheader("🚨 Claim With Highest Complexity")
    max_row = results_df.loc[results_df["complexity_score"].idxmax()]
    st.write(max_row["claim_note"])
    st.write(f"Complexity Score: {max_row['complexity_score']} — {max_row['complexity_reason']}")

    # ---------------------------------
    # Contributing Factor Analysis
    # ---------------------------------
    st.subheader("🧩 Contributing Factor Frequency")

    factor_list = []
    for row in results_df["contributing_factors"]:
        if row != "None":
            factor_list.extend(row)

    if len(factor_list) == 0:
        st.info("No contributing factors found in dataset.")
    else:
        factor_freq = pd.Series(factor_list).value_counts().reset_index()
        factor_freq.columns = ["factor", "count"]

        chart = (
            alt.Chart(factor_freq)
            .mark_bar()
            .encode(
                x="count:Q",
                y=alt.Y("factor:N", sort="-x"),
            )
            .properties(height=300)
        )

        st.altair_chart(chart, use_container_width=True)

    # Show full scored table
    st.subheader("📋 Scored Dataset")
    st.dataframe(results_df)

    st.success("Analysis complete! Saved to scored_claims.json")
