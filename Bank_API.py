from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()
df = pd.read_csv("banks.csv")

@app.exception_handler(404) #if any page that doesnt exist is accessed
def not_found_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=404,
        content={
            "error": "Endpoint not found",
            "message": f"The requested URL {request.url.path} doesn't exist",
            "valid_endpoints": [
                "/banks",
                "/banks/ifsc={ifsc_code}",
                "/banks/bank_id={bank_id}",
                "/docs"]
        },
    )

@app.get("/")
def home(): #home page
    return JSONResponse(content={"/banks":"For all entries",
            "/banks/ifsc={ifsc code here}":"For banks with specified ifsc code",
            "/banks/bank_id={bank id here}":"For banks with specified bank id",
            "/docs":"UI experience"})

@app.get("/banks") #for entering limit endpoint is like /banks?limit=500
def get_all_banks(limit: str = '100'): #returns upto "limit" number of entries
    try:
        limit = int(limit)
    except:
        raise HTTPException(status_code=400, detail="Limit must be integer in range 1-8250") #error is raised if some number is not given in limit parameter

    if limit <= 0 or limit > 8250: #to ensure less load on the server
        raise HTTPException(status_code=400, detail="Limit must be integer in range 1-8250")
    return df.head(limit).to_dict(orient="records")


@app.get("/banks/ifsc={ifsc}")
def get_bank_by_ifsc(ifsc: str): #returns the bank details for bank with specific ifsc code
    bank = df[df["ifsc"] == ifsc]
    if bank.empty:
        raise HTTPException(status_code=404, detail="IFSC not found") #error 404 if nothing is found
    return bank.to_dict(orient="records")


@app.get("/banks/bank_id={bank_id}")
def get_banks_by_id(bank_id: int):#finds banks with specific bank id
    banks = df[df["bank_id"] == bank_id]
    if banks.empty:
        raise HTTPException(status_code=404, detail="Bank id not found") #error 404 if nothing is found
    return banks.to_dict(orient="records")
