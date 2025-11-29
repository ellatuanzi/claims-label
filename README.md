# Claim Factor Analyzer

An AI-powered tool that automatically analyzes insurance claim adjuster notes to identify contributing factors, assess claim clarity and complexity, and generate insights using OpenAI's GPT models.

## Features

- **🤖 AI-Powered Analysis**: Uses GPT models to analyze claim notes
- **📊 Two Interactive Apps**:
  - **App 1**: Batch processing with binary indicators for multiple claims
  - **App 2**: Single claim scoring with clarity, complexity, and contributing factors
- **📈 Advanced Analytics**: Visual dashboards with charts and statistics
- **🔍 Pre-Accident Focus**: Identifies only factors explicitly stated before accidents

## Project Structure

```
claim label/
├── app.py                          # Batch claim analysis dashboard
├── app2.py                         # Single claim scoring app
├── data_generation.py              # Script to generate synthetic claim data
├── synthetic_claim_data.json       # JSON dataset of synthetic claims
├── synthetic_claim_data.csv        # CSV format of synthetic claims
├── labeled_claim_data.csv          # Labeled claims with binary indicators
├── scored_claims.json              # Output from batch scoring
├── .env.example                    # Environment variable template
└── README.md                       # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "claim label"
   ```

2. **Install required packages**
   ```bash
   pip install pandas openai streamlit python-dotenv altair
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

### App 1: Batch Claim Analysis (app.py)

Process multiple claims at once with comprehensive analytics.

**Run the app:**
```bash
streamlit run app.py
```

**Features:**
- Loads claim dataset from JSON file
- Scores all claims using GPT-4o-mini
- Generates aggregate statistics:
  - Average clarity and complexity scores
  - Claims with lowest clarity
  - Claims with highest complexity
  - Contributing factor frequency analysis
- Saves results to `scored_claims.json`

**Screenshot:**
![Batch Analysis Dashboard](screenshots/Screenshot 2025-11-28 at 8.39.23 PM.png)

### App 2: Advanced Claim Analysis (app2.py)

Comprehensive claim evaluation with multiple analysis modes.

**Run the app:**
```bash
streamlit run app2.py
```

**Two Modes Available:**

#### 1. Single Claim Analysis
Evaluate individual claims with detailed scoring:
- **Clarity Score (1-5)**: How clearly the note is written
- **Complexity Score (1-5)**: How complex the incident is  
- **Contributing Factors**: Pre-accident factors explicitly mentioned
- **Inconsistency Detection**: Identifies contradictions in the narrative
- **Structured Data Extraction**: Extracts key fields (date, location, injuries, weather, etc.)

#### 2. Batch Folder Analysis
Upload and process multiple claims at once:
- Processes JSON files (single object or arrays)
- Supports both `claim_note` and `claim_text` field names
- Generates aggregate analytics:
  - Average clarity and complexity scores
  - Contributing factor frequency distribution
  - Inconsistency counts across all claims
- Sample extracted information display

**How to Use Batch Mode:**
1. Prepare JSON file(s) with claim data
2. Upload via the file uploader
3. View aggregated results and analytics

**Screenshot:**
![Advanced Claim Analysis](screenshots/app2-advanced.png)

### Data Generation

Create synthetic claim data for testing:

```bash
python data_generation.py
```

This creates both `synthetic_claim_data.csv` and `synthetic_claim_data.json` with sample claim notes.

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
- python-dotenv
- altair (for visualizations)
- httpx (for OpenAI client)

## Models Used

- **App 1 (Batch Processing)**: GPT-4o-mini with standard completions
- **App 2 (Advanced Analysis)**: GPT-4o-mini with JSON mode for structured output

## Key Features by App

### App 1 (app.py)
- ✅ Batch processing of entire datasets
- ✅ Visual analytics with Altair charts
- ✅ Contributing factor frequency analysis
- ✅ Identifies claims with clarity/complexity issues
- ✅ Exports results to JSON

### App 2 (app2.py)
- ✅ Single claim or batch file processing
- ✅ Inconsistency detection in claim narratives
- ✅ Structured information extraction (dates, locations, etc.)
- ✅ More detailed field extraction (13+ data fields)
- ✅ Two processing modes (single/batch)
- ✅ Aggregate statistics for batch uploads

## Example Analysis

### App 1 Output Example
```json
{
  "id": 2,
  "claim_note": "Driver drifted out of lane and sideswiped a box truck...",
  "clarity_score": 4,
  "clarity_reason": "Note provides clear sequence of events with specific details",
  "complexity_score": 2,
  "complexity_reason": "Simple single-vehicle incident with clear cause",
  "contributing_factors": ["distraction", "phone use"]
}
```

### App 2 Output Example
```json
{
  "clarity_score": 4,
  "clarity_reason": "Clear and well-documented incident description",
  "complexity_score": 3,
  "complexity_reason": "Moderate complexity with multiple vehicles and injury claims",
  "contributing_factors": ["fatigue", "following distance"],
  "inconsistencies": ["Driver stated 'no injuries' but later reported neck pain"],
  "extracted_info": {
    "incident_date": "2024-06-15",
    "location": "I-75 northbound",
    "vehicles_involved": "2",
    "injuries": "minor neck pain",
    "weather": "light rain",
    "road_condition": "wet",
    "speed": null,
    "police_report": "yes",
    "liability_statement": "driver admits fault",
    "citation": "following too closely",
    "cargo_load": null,
    "distraction": null,
    "mechanical_issue": null
  }
}
```

## Screenshots

Screenshots are available in the `screenshots/` folder:

1. **app.py** - Batch analysis dashboard with charts and statistics
2. **app2.py** - Advanced analysis with single claim and batch modes

To add your own screenshots:
1. Run the apps and capture screenshots
2. Save them in the `screenshots/` folder
3. Update the image references in this README

## Contributing Factors Examples

The system can identify various contributing factors when explicitly mentioned in pre-accident context:

- **Distraction**: Phone use, GPS adjustment, passenger interaction, eating/drinking
- **Fatigue**: Long driving hours, drowsiness, lack of sleep, extended duty time
- **Weather**: Rain, ice, fog, snow, poor visibility, sun glare
- **Road Conditions**: Debris, poor lighting, wet/icy surfaces, road design, sharp curves
- **Mechanical**: Brake failure, tire blowout, equipment malfunction, brake fade
- **Speed**: Excessive speed, following too closely, tailgating
- **Impairment**: Not explicitly detected (requires careful analysis of wording)

## Inconsistency Detection (App 2)

App 2 can identify contradictions in claim narratives:
- Conflicting injury statements ("no injuries" vs. later "neck pain")
- Vehicle count mismatches (single vs. multiple vehicles)
- Timeline inconsistencies
- Location discrepancies
- Conflicting liability statements

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
