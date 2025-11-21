import pandas as pd
from openai import OpenAI
import streamlit as st
import os

# Clear any proxy environment variables that might interfere
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

# 设置 OpenAI API 密钥
# Get API key from environment variable or Streamlit secrets
api_key = os.environ.get('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', None)

if not api_key:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable or add it to Streamlit secrets.")
    st.stop()

os.environ['OPENAI_API_KEY'] = api_key

# Initialize OpenAI client with explicit http_client to avoid proxy issues
try:
    client = OpenAI()
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    client = None

# 定义调用 ChatGPT 的函数来给 note 打标签的 prompt 和逻辑
def label_claim_note(note):
    prompt = (
        f"Based on the following claim adjuster note, identify potential contributing factors such as 'Distraction', 'Fatigue', 'Light Condition', or 'Roadway Design'. If you find any other relevant contributing factors, feel free to include them as well. Please label the contributing factors based strictly on what is explicitly mentioned in the claim note. Do not infer or add extra labels beyond the given information. Here is the note: '{note}'"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    label = response.choices[0].message.content.strip()
    return label


data = pd.read_csv("synthetic_claim_data.csv")


data['Label'] = data['ClaimNote'].apply(label_claim_note)

# Create binary indicator columns for key factors
key_factors = ['Distraction', 'Fatigue', 'Light Condition', 'Roadway Design']

for factor in key_factors:
    # Create a column name (e.g., 'Has_Distraction')
    column_name = f'Has_{factor.replace(" ", "_")}'
    # Check if the factor appears in the Label (case-insensitive)
    data[column_name] = data['Label'].str.contains(factor, case=False, na=False).astype(int)

data.to_csv("labeled_claim_data.csv", index=False)

def main():
    st.title('Claim Analysis Dashboard')
    
    # Display binary indicators summary
    st.subheader('Contributing Factors Analysis')
    factor_columns = [col for col in data.columns if col.startswith('Has_')]
    
    if factor_columns:
        # Get counts for each factor
        factor_summary = data[factor_columns].sum().sort_values(ascending=False)
        
        # Rename columns for better display
        factor_summary.index = factor_summary.index.str.replace('Has_', '').str.replace('_', ' ')
        
        # Display as bar chart
        st.bar_chart(factor_summary)
        
        # Display the counts table
        st.subheader('Factor Counts')
        st.write(factor_summary)
        
        # Display statistics
        st.subheader('Statistics')
        total_claims = len(data)
        st.metric("Total Claims", total_claims)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Claims with Multiple Factors", 
                     (data[factor_columns].sum(axis=1) > 1).sum())
        with col2:
            st.metric("Claims with No Factors", 
                     (data[factor_columns].sum(axis=1) == 0).sum())
        
        # Display the dataset with binary indicators
        st.subheader('Detailed Claim Data')
        st.dataframe(data[['ClaimID', 'ClaimNote'] + factor_columns])

if __name__ == '__main__':
    main()
