# Claim Factor Analyzer

An AI-powered tool that automatically analyzes insurance claim adjuster notes to identify contributing factors such as Distraction, Fatigue, Light Condition, and Roadway Design using OpenAI's GPT model.

## Features

- **Automated Labeling**: Uses GPT-3.5-turbo to analyze claim notes and identify contributing factors
- **Binary Indicators**: Creates binary columns for each key factor for easy analysis
- **Interactive Dashboard**: Streamlit-based visualization showing:
  - Contributing factors distribution
  - Factor counts and statistics
  - Claims with multiple factors
  - Detailed claim data with binary indicators

## Project Structure

```
claim label/
├── app.py                      # Main Streamlit application
├── data_generation.py          # Script to generate synthetic claim data
├── synthetic_claim_data.csv    # Generated synthetic claims
├── labeled_claim_data.csv      # Labeled claims with binary indicators
└── README.md                   # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "claim label"
   ```

2. **Install required packages**
   ```bash
   pip install pandas openai streamlit
   ```

3. **Set up OpenAI API Key**
   
   You have two options:
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   
   **Option B: Using .env file**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key
   
   **Option C: Streamlit Secrets**
   - Create `.streamlit/secrets.toml`:
     ```toml
     OPENAI_API_KEY = "your-api-key-here"
     ```

## Usage

### 1. Generate Synthetic Data

Run the data generation script to create sample claim notes:

```bash
python data_generation.py
```

This creates `synthetic_claim_data.csv` with 11 sample claim notes.

### 2. Run the Streamlit Dashboard

Launch the interactive dashboard:

```bash
streamlit run app.py
```

The app will:
- Load the synthetic claim data
- Analyze each claim note using GPT-3.5-turbo
- Create binary indicator columns for key factors
- Display visualizations and statistics
- Save the results to `labeled_claim_data.csv`

### 3. View the Dashboard

The dashboard will open in your browser (typically at `http://localhost:8501`) and display:

- **Contributing Factors Analysis**: Bar chart showing frequency of each factor
- **Factor Counts**: Numerical breakdown of each contributing factor
- **Statistics**: 
  - Total claims processed
  - Claims with multiple factors
  - Claims with no factors identified
- **Detailed Claim Data**: Table with claim notes and binary indicators

## Key Contributing Factors

The system identifies the following factors:

- **Distraction**: Driver distraction (navigation, talking, etc.)
- **Fatigue**: Driver tiredness or drowsiness
- **Light Condition**: Poor lighting or visibility issues
- **Roadway Design**: Road design problems (sharp turns, etc.)

## Binary Indicators

For each claim, the following binary columns are created:

- `Has_Distraction` (0 or 1)
- `Has_Fatigue` (0 or 1)
- `Has_Light_Condition` (0 or 1)
- `Has_Roadway_Design` (0 or 1)

## Requirements

- Python 3.8+
- pandas
- openai >= 2.0.0
- streamlit
- httpx (for OpenAI client)

## Configuration

### Customizing the Prompt

Edit the `label_claim_note()` function in `app.py` to modify how the AI analyzes claims.

### Adding More Factors

To track additional contributing factors:

1. Add the factor name to the `key_factors` list in `app.py`
2. The system will automatically create a corresponding binary column

## Example Output

### Sample Claim Note
```
"The driver mentioned feeling extremely tired after driving for over 12 hours without a break. 
They believed this fatigue might have caused them to lose focus on the road."
```

### Identified Factors
- `Has_Fatigue`: 1
- `Has_Distraction`: 0
- `Has_Light_Condition`: 0
- `Has_Roadway_Design`: 0

## Notes

- The first run will call the OpenAI API for each claim, which may take a few moments
- API calls incur costs based on OpenAI's pricing
- Results are cached in `labeled_claim_data.csv` for future reference

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
