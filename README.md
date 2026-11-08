# AI Lead Scoring Agent

An intelligent lead scoring system that analyzes company data using AI to predict lead quality and priority.

## Features

- Automated company research and data collection
- AI-powered lead scoring based on multiple factors
- CRM synchronization capabilities
- Configurable pipeline with modular components

## Project Structure

```
ai-lead-scoring-agent/
├── data/           # Input/output data files
├── logs/           # Application logs
├── src/            # Source code
│   ├── config.py       # Configuration management
│   ├── research.py     # Company research functionality
│   ├── scoring.py      # Lead scoring logic
│   ├── pipeline.py     # Main processing pipeline
│   ├── crm_sync.py     # CRM integration
│   └── main.py         # Application entry point
├── .env            # Environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`

## Usage

```bash
python src/main.py
```