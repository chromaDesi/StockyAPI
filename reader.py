from fastapi import FastAPI, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from scraperhelper import (
    getFinvizQuote,
    getGoogleQuote,
    currency_rates,
    scrape_finviz_detailed,
    greed_index
)

app = FastAPI(
    title="StockyAPI Reader Service",
    version="1.0.0",
    description="Educational market data API. Alpha testing phase."
)

# --------------------
# Root & Health
# --------------------

@app.get("/")
def root():
    return {"message": "Welcome to the StockyAPI Reader Service"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

# --------------------
# Quotes
# --------------------

@app.get("/quotes/{ticker}")
async def get_quote(
    ticker: str,
    source: str = Query(..., description="google or finviz"),
    exchange: str | None = Query(None, description="Required for Google Finance (Not used for Finviz)"),
    period: str | None = Query(None, description="Optional period for Finviz or Google Finance (Different formats)")
):
    try:
        if source == "google":
            if period is None:
                period = "1D"
            if not exchange:
                raise HTTPException(
                    status_code=400,
                    detail="exchange parameter is required for Google Finance"
                )
            return await run_in_threadpool(getGoogleQuote, ticker, exchange, period)

        elif source == "finviz":
            if period is None:
                period = "d"
            return await run_in_threadpool(getFinvizQuote, ticker, period)

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid source. Use 'google' or 'finviz'"
            )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Detailed Quotes
# --------------------

@app.get("/quotes/{ticker}/details")
async def get_quote_details(
    ticker: str,
    period: str = Query(..., description="Time period for detailed Finviz data")
):
    try:
        return await run_in_threadpool(scrape_finviz_detailed, ticker, period)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Currency Rates
# --------------------

@app.get("/currency-rates")
async def get_currency_rates():
    try:
        return await run_in_threadpool(currency_rates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Sentiment
# --------------------

@app.get("/sentiment/greed-index")
async def get_greed_index():
    try:
        return await run_in_threadpool(greed_index)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))