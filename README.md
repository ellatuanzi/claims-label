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

### App 2: Single Claim Scoring (app2.py)

Evaluate individual claims with detailed scoring.

**Run the app:**
```bash
streamlit run app2.py
```

**Features:**
- Interactive text input for claim notes
- Real-time LLM scoring with:
  - **Clarity Score (1-5)**: How clearly the note is written
  - **Complexity Score (1-5)**: How complex the incident is
  - **Contributing Factors**: List of pre-accident factors
- JSON response format for easy integration
- Debug view showing raw model output

**Screenshots:**

#### Input Interface
![Single Claim Input](screenshots/app2-input.png)

#### Results Display
![Single Claim Results](screenshots/app2-results.png)

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

- **App 1 (Batch Processing)**: GPT-4o-mini
- **App 2 (Single Scoring)**: GPT-3.5-turbo with JSON mode

## Example Analysis

### Input Claim Note
```
Driver drifted out of lane and sideswiped a box truck. 
Insured admitted he was checking his phone for directions. 
No injuries. Damage to right side mirror and panel.
```

### Output (App 2)
```json
{
  "clarity_score": 4,
  "clarity_reason": "The note clearly describes the incident with specific details about the collision and damage",
  "complexity_score": 2,
  "complexity_reason": "Simple single-vehicle incident with clear liability and no injuries",
  "contributing_factors": ["distraction", "phone use"]
}
```

## Screenshots

To add screenshots to this README:

1. Create a `screenshots` folder in the project root
2. Take screenshots of:
   - `app2-input.png` - The text input interface
   - `app2-results.png` - The results display with scores
   - `app1-dashboard.png` - The batch analysis dashboard
3. Save them in the screenshots folder

## Contributing Factors Examples

The system can identify various contributing factors when explicitly mentioned:
- **Distraction**: Phone use, GPS adjustment, passenger interaction
- **Fatigue**: Long driving hours, drowsiness, lack of sleep
- **Weather**: Rain, ice, fog, poor visibility
- **Road Conditions**: Debris, poor lighting, road design
- **Mechanical**: Brake failure, tire blowout
- **Speed**: Excessive speed, following too closely

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
