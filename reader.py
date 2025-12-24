from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from scraperhelper import scrape_stock_data, jsonWrapper
'''import firebase_admin
from firebase_admin import firestore, credentials


#to run api use py -m uvicorn reader:app --reload
#for docs use py -m uvicorn reader:app --reload and go to localhost:8000/docs#/


cred = credentials.Certificate("google-services.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
'''
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the StockyAPI Reader Service"}


@app.get("/quotes/{ticker_symbol}/{exchangecode}")
async def get_qoute(ticker_symbol: str, exchangecode: str):
    try:
        soup = await run_in_threadpool(
            scrape_stock_data,
            ticker_symbol,
            exchangecode)
        currprice = soup.find_all('div', class_='fxKbKc')
        pe = soup.find_all('div', class_='P6K39c')
        return jsonWrapper(currprice, pe)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


