# 📈 StockyAPI

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)

> ⚠️ **Early Development Notice**  
> StockyAPI is currently in **early development (alpha)**. APIs, schemas, and features may evolve as the project matures. Feedback and contributions are welcome.

**StockyAPI** is a lightweight, educational-first market data API designed for **students and early-career developers** who want to build finance, data science, and machine learning projects *without fighting messy data*.

Instead of exposing raw scraped fields, StockyAPI provides **normalized, enriched, and beginner-friendly stock data** with built-in explanations, reliability metadata, and derived signals.

> Think of it as *“market data that actually makes sense.”*

---

## ✨ Why StockyAPI?

Most free finance APIs and scrapers:
- return inconsistent schemas
- expose unexplained financial jargon
- silently fail when sources change
- force students to clean data before learning anything

**StockyAPI solves this by:**
- normalizing data across multiple public sources
- adding confidence and freshness indicators
- exposing derived signals (momentum, valuation)
- embedding explanations directly in responses

This makes it ideal for:
- class projects
- hackathons
- ML experiments
- portfolio dashboards
- interview demos

---

## 🚀 Features

### ✅ Normalized Quote Schema
Stable field names across all sources so your code doesn’t break.

### ✅ Multi-Source Aggregation
Currently aggregates public market data from:
- Google Finance
- Finviz

(Sources can be swapped without breaking the API contract.)

### ✅ Reliability Metadata
Each response includes:
- last updated timestamp
- confidence score
- data sources used
- fallback indicators

### ✅ Derived Market Signals
Beginner-friendly computed insights:
- daily percent change
- valuation category (cheap / fair / expensive)
- short-term momentum
- volatility level

### ✅ Educational Context
Optional learning notes explaining what each metric means and how it’s used.

---

## 🧠 Example Response

```json
{
  "ticker": "AAPL",
  "price": 189.24,
  "change_percent": 1.42,

  "valuation": {
    "pe_ratio": 28.4,
    "category": "overvalued",
    "explanation": "P/E is higher than the sector median"
  },

  "signals": {
    "momentum_1d": "bullish",
    "volatility": "moderate"
  },

  "learning_notes": {
    "pe_ratio": "Price-to-Earnings compares market price to earnings per share.",
    "momentum_1d": "Measures short-term price trend direction."
  },

  "reliability": {
    "confidence": 0.91,
    "sources": ["google_finance", "finviz"],
    "last_updated": "2025-12-25T03:14:00Z"
  }
}
