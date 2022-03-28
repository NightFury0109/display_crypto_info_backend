from datetime import datetime, timedelta, date
import requests
from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/f1")
def f1(name: Optional[str] = "bitcoin", before: Optional[date] = date.today(), limit: Optional[int] = 20):
    try:
        if limit < 1:
            return {"detail":[{"loc":["query","limit"],"msg":"value is not valid: must be > 0","type":"type_error.integer"}]}
        if date.today() < before:
            return {"detail":[{"loc":["query","before"],"msg":"invalid date: before > current date","type":"value_error.date"}]}
        given_date_str = before.strftime('%Y-%m-%d')
        previous_day = before - timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        previous = before - timedelta(days=limit)
        previous_str = previous.strftime('%Y-%m-%d')
        response = requests.get(f"https://data.messari.io/api/v1/assets/{name}/metrics/price/time-series?start={previous_str}&end={previous_day_str}&interval=1d")
        response = response.json()
        if "data" in response:
            result_data = response["data"]
            high_values = [value[4] for value in result_data["values"]]
            avg = sum(high_values) / len(high_values)
            return {
                "Symbol": result_data['symbol'],
                "Name": result_data['name'],
                "Date": given_date_str,
                f"{limit} Moving Average": avg
            }
        else:
            return {
                "error_code": response["status"]["error_code"], 
                "error_message": response["status"]["error_message"] 
            }
    except:
        return {"detail":"Not Found"}


@app.get("/f2")
def f2(name: Optional[str] = "bitcoin"):
    try:
        before = date.today()
        given_date_str = before.strftime('%Y-%m-%d')
        previous_day = before - timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        previous = before - timedelta(days=50)
        previous_str = previous.strftime('%Y-%m-%d')
        response = requests.get(f"https://data.messari.io/api/v1/assets/{name}/metrics/price/time-series?start={previous_str}&end={previous_day_str}&interval=1d")
        response = response.json()
        if "data" in response:
            result_data = response["data"]
            high_values = [value[4] for value in result_data["values"]]
            avg_20 = sum(high_values[0:20]) / len(high_values[0:20])
            avg_50 = sum(high_values) / len(high_values)
            stock = "20 moving average is greater than 50 moving average it's bullish" if avg_20 > avg_50 else "20 moving average is less than 50 moving average it's bearish"
            return {
                "Symbol": result_data['symbol'],
                "Name": result_data['name'],
                "20 moving average": avg_20,
                "50 moving average": avg_50,
                "Stock": stock 
            }
        else:
            return {
                "error_code": response["status"]["error_code"], 
                "error_message": response["status"]["error_message"] 
            }
    except:
        return {"detail":"Not Found"}


@app.get("/f3")
def f3(name: Optional[str] = "bitcoin"):
    try:
        before = date.today()
        given_date_str = before.strftime('%Y-%m-%d')
        previous = before - timedelta(days=50)
        previous_str = previous.strftime('%Y-%m-%d')
        response = requests.get(f"https://data.messari.io/api/v1/assets/{name}/metrics/price/time-series?start={previous_str}&end={given_date_str}&interval=1d")
        response = response.json()
        if "data" in response:
            result_data = response["data"]
            high_values = [value[4] for value in result_data["values"]]
            avg_20 = sum(high_values[1:21]) / len(high_values[1:21])
            avg_50 = sum(high_values[1:]) / len(high_values[1:])
            stock = "bullish" if avg_20 > avg_50 else "bearish"
            decision = "buy" if stock == "bullish" and result_data["values"][0][4] > avg_20 and result_data["values"][0][5] > result_data["values"][1][5] else "sell"
            return {
                "Symbol": result_data['symbol'],
                "Name": result_data['name'],
                "Buy conditions": [
                    {
                        "Description": "20 moving average is greater than 50 moving avergae",
                        "Success": True if stock == "bullish" else False
                    },
                    {
                        "Description": "Current price is above 20 and 50 moving averages",
                        "Success": True if result_data["values"][0][4] > avg_20 else False
                    },
                    {
                        "Description": "Current volume is greater than yesterdays volume",
                        "Success": True if result_data["values"][0][5] > result_data["values"][1][5] else False
                    }
                ],
                "Decision": decision
            }
        else:
            return {
                "error_code": response["status"]["error_code"], 
                "error_message": response["status"]["error_message"] 
            }
    except:
        return {"detail":"Not Found"}
