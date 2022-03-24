# Import useful modules and APIs
import pandas as pd
from sec_api import QueryApi
from sec_api import RenderApi ## couldn't get this to work to automatically download the reports
import csv

# Import scores from sustainalytics csv - note filename MAY NEED TO CHANGE
scores = pd.read_csv("Sustainalytics_scores.csv", sep=',', encoding='utf-8')

# Initialise instance of QueryApi with your own personal api-key - YOU NEED TO CHANGE
queryApi = QueryApi(api_key="ea7e88eafa2457053be77c61ced50251b313da7a476f9fbbe7fe551a8a9029a2")

# renderApi = RenderApi(api_key="ea7e88eafa2457053be77c61ced50251b313da7a476f9fbbe7fe551a8a9029a2")
## couldn't get this to work to automatically download the reports

# number of URLs of reports to retrieve
n = 1
tickers = scores["Ticker"][:n]

# Initialise dictionary to store retrieved URLs
data = {}

# Loop through the n companies
for company in tickers:
    # Build up the query string
    ticker_string = f'ticker: {company}'
    full_string = ticker_string + ' AND filedAt:{2021-01-01 TO 2021-12-31} AND formType:\"10-K\"'
    query = {}
    query["query"] = full_string
    query_string = {}
    query_string["query_string"] = query
    full_query = {}
    full_query["query"] = query_string

    # Call the queryAPI to get company details
    filings = queryApi.get_filings(full_query)

    # Store company the URL in a dictionary
    data[company] = filings["filings"][0]["linkToFilingDetails"]


# Download the URLs into a csv
with open('annual_report_urls.csv', 'w', newline='') as f:
    col_names = ['Ticker', 'Annual Report Url']
    new_f = csv.DictWriter(f, fieldnames=col_names)

    new_f.writeheader()
    for ticker in data:
        new_f.writerow({'Ticker': ticker, 'Annual Report Url': data[ticker]})








