# GameStop Meme Stock Q&A

AI-powered chat interface for the GameStop short squeeze case study (MGMT 69000: Mastering AI for Finance, Purdue University).

## Overview

Interactive Streamlit app that answers questions about the January 2021 GameStop meme stock short squeeze using OpenAI. Features the DRIVER framework, transfer entropy analysis, market microstructure deep dives, and a personality that has opinions about Robinhood halting the buy button.

## Setup

```bash
pip install -r requirements.txt
```

Configure your API key in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
python -m pytest test_app.py -v
python -m ruff check .
```

## Architecture

```
Case Markdown → System Prompt → Streamlit Chat UI → OpenAI API
                                      ↕
                              Session State (audit trail w/ timestamps)
```

## Features

- Structured Q&A with headers, bullet points, and data-rich answers
- Interactive charts (GME price timeline, short interest, meme stock returns)
- Timestamped audit trail on every message
- Question mark animation on new questions
- Keyword-specific toast reactions
- Animated contagion flow diagram (Reddit → Twitter → Media → Meme Stocks)
- Scrolling ticker tape with key metrics
- Dark theme with animated gradient background
