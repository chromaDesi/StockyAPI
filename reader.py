from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from scraperhelper import getFinvizQuote, getGoogleQuote, currency_rates, scrape_finviz_detailed
'''import firebase_admin
from firebase_admin import firestore, credentials


#to run api use py -m uvicorn reader:app --reload
#for docs use py -m uvicorn reader:app --reload and go to localhost:8000/docs#/


cred = credentials.Certificate("google-services.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
'''
app = FastAPI(title="StockyAPI Reader Service", version="1.0.0", description="API Service for scraping stock data from Google Finance and Finviz. Alpha Testing Phase.")


@app.get("/")
def root():
    return {"message": "Welcome to the StockyAPI Reader Service"}


@app.get("/quotes/google/{ticker_symbol}&{exchangecode}")
async def get_qoute(ticker_symbol: str, exchangecode: str):
    try:
        return await run_in_threadpool(
            getGoogleQuote,
            ticker_symbol,
            exchangecode)
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/qoutes/finviz/detailed/{ticker_symbol}&{pd}")
async def get_finviz_detailed_qoute(ticker_symbol: str, pd: str):
    return scrape_finviz_detailed(ticker_symbol, pd)

@app.get("/qoutes/finviz/{ticker_symbol}&{pd}")
async def get_finviz_qoute(ticker_symbol: str, pd: str):
    try:
        return await run_in_threadpool(
            getFinvizQuote,
            ticker_symbol,
            pd)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.get("/finviz/currency/rates")
async def get_currency_rates():
    return currency_rates()


