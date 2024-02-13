from fastapi import APIRouter, HTTPException, Query
from modules.data_toolkit.nse.helper import fetch_data_from_nse, convert_dataframe_to_dict, transform_financial_year
from fastapi.responses import JSONResponse
import requests
import pandas as pd
import re
import json

router = APIRouter()

    
def security_wise_archive(symbol, start_date, end_date, series="ALL"):   
    base_url = "https://www.nseindia.com/api/historical/securityArchives"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}&symbol={symbol.upper()}&dataType=priceVolumeDeliverable&series={series.upper()}"
    response = fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/security-archives?symbol=TCS&start_date=04-01-2024&end_date=14-01-2024&series=ALL
@router.get("/equities/security-archives")
def get_security_wise_archive(
    symbol: str = Query(..., title="Symbol", description="Stock symbol"),
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),
    series: str = Query("ALL", title="Series", description="Stock series")
):
    try:
        historical_data = security_wise_archive(symbol, start_date, end_date, series)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching security-wise archive data: {e}")
    
    
def bulk_deals_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/bulk-deals"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/bulk-deals-archives?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/bulk-deals-archives")
def get_bulk_deals_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = bulk_deals_archives(start_date, end_date)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bulk-deals archive data: {e}")
    
    
def block_deals_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/block-deals"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


# Example usage - http://localhost:8000/equities/block-deals-archives?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/block-deals-archives")
def get_block_deals_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = block_deals_archives(start_date, end_date)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blovk deals archive data: {e}")
    

def short_selling_archives(start_date, end_date):
    base_url="https://www.nseindia.com/api/historical/short-selling"
    customized_request_url = f"{base_url}?from={start_date}&to={end_date}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/short-selling?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/short-selling-archives")
def get_short_selling_archives(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = short_selling_archives(start_date, end_date)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching short-selling archive data: {e}")
    

def corporate_actions(start_date, end_date):
    base_url = "https://www.nseindia.com/api/corporates-corporateActions"
    
    customized_request_url = f"{base_url}?index=equities&from={start_date}&to={end_date}"
    response = fetch_data_from_nse(customized_request_url)
    
    if not response:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    if isinstance(response, list):
        payload = response
    else:
        payload = response.get('data', [])
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/corporate-actions?start_date=28-01-2024&end_date=04-02-2024
@router.get("/equities/corporate-actions")
def get_corporate_actions(
    start_date: str = Query(..., title="From Date", description="Start date for historical data in dd-mm-yyyy format"),
    end_date: str = Query(..., title="To Date", description="End date for historical data in dd-mm-yyyy format"),  
):
    try:
        historical_data = corporate_actions(start_date, end_date)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching corporate actions data: {e}")
    

def nse_monthly_most_active_securities():
    request_url = "https://www.nseindia.com/api/historical/most-active-securities-monthly"
    response = fetch_data_from_nse(request_url)
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)
    

# Example usage - http://localhost:8000/equities/most-active-securities
@router.get("/equities/most-active-securities")
def get_nse_monthly_most_active_securities():
    try:
        historical_data = nse_monthly_most_active_securities()
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly most active securities data: {e}")
    
    
def nse_monthly_advances_and_declines(year):
    base_url="https://www.nseindia.com/api/historical/advances-decline-monthly"
    customized_request_url = f"{base_url}?year={year}"
    response=fetch_data_from_nse(customized_request_url)
    
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No data found for the specified parameters.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/advances-declines?year=2024
@router.get("/equities/advances-declines")
def get_nse_monthly_advances_and_declines(
    year: str = Query(..., title="Year", description="Year for historical data in format YYYY"), 
):
    if not re.match(r"\d{4}", year):
        raise HTTPException(status_code=422, detail="Invalid year format. Please use 'YYYY' format.")
    
    try:
        historical_data = nse_monthly_advances_and_declines(year)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching advances and decline data: {e}")
    
    
def nse_capital_market_monthly_settlement_stats(financial_year):
    base_url = "https://www.nseindia.com/api/historical/monthly-sett-stats-data"
    customized_request_url = f"{base_url}?finYear={financial_year}"
    response = fetch_data_from_nse(customized_request_url)
    payload = response.get('data', [])
    
    if not payload:
        raise HTTPException(status_code=404, detail=f"No capital market settlement statistics found.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/monthly-settlement-stats/capital-market?financial_year=2022-2023
@router.get("/equities/monthly-settlement-stats/capital-market")
def get_nse_capital_market_monthly_settlement_stats(
    financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
):
    if not re.match(r"\d{4}-\d{4}", financial_year):
        raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
    
    try:
        historical_data = nse_capital_market_monthly_settlement_stats(financial_year)
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for capital market: {e}")


def nse_fno_monthly_settlement_stats(financial_year):
    from_date, to_date = transform_financial_year(financial_year)
    base_url = "https://www.nseindia.com/api/financial-monthlyStats"
    customized_request_url = f"{base_url}?from_date={from_date}&to_date={to_date}"
    response = fetch_data_from_nse(customized_request_url)
    payload = response 
    
    if not payload:
        raise HTTPException(status_code=404, detail="No monthly settlement statistics found.")
    
    return pd.DataFrame(payload)


#Example usage - http://localhost:8000/equities/monthly-settlement-stats/fno?financial_year=2022-2023
@router.get("/equities/monthly-settlement-stats/fno")
def get_nse_fno_monthly_settlement_stats(
    financial_year: str = Query(..., title="Year", description="Financial Year for historical data in format YYYY-YYYY"), 
):
    if not re.match(r"\d{4}-\d{4}", financial_year):
        raise HTTPException(status_code=422, detail="Invalid financial year format. Please use 'YYYY-YYYY' format.")
    
    try:
        historical_data = nse_fno_monthly_settlement_stats(financial_year)
        
        if not isinstance(historical_data, pd.DataFrame):
            raise HTTPException(status_code=404, detail="No data found.")
        
        rounded_data = convert_dataframe_to_dict(historical_data)
        return JSONResponse(content={"data": rounded_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching monthly settlement statistics for future & options: {e}")
    

def pcr_stocks_scraper(symbol):
    url = 'https://www.nseindia.com/api/option-chain-equities?symbol=' + symbol
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'en-US,en;q=0.9'
    }
    request = requests.get("https://www.nseindia.com", timeout=10, headers=headers)
    cookies = dict(request.cookies)
    response = requests.get(url, headers=headers, cookies= cookies).content
    
    data = json.loads(response.decode('utf-8'))
    totCE = data['filtered']['CE']['totOI']
    totPE = data['filtered']['PE']['totOI']

    pcr= totPE/totCE
    return round(pcr,3)


#Example usage - http://127.0.0.1:8000/equities/stock-pcr?symbol=RELIANCE
@router.get("/equities/stock-pcr")
def get_pcr(symbol: str = Query(..., title="Symbol", description="Stock symbol")):
    pcr_value = pcr_stocks_scraper(symbol)
    return {"symbol": symbol, "pcr_value": pcr_value}