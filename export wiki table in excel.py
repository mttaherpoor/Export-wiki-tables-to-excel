import requests
from bs4 import BeautifulSoup
import pandas as pd

def tables_wiki(url):
    # Define the URL of the Wikipedia page
    wiki_url = url
    
    # Send a GET request to the URL and retrieve the page content
    response = requests.get(wiki_url)
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all tables on the page
    tables = soup.find_all("table", {"class": "wikitable"})
    
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Loop through each table and read it into a Pandas DataFrame
    for table in tables:
        # Extract country name from the table header if available
        header_element = table.find_previous("h2")
        if header_element:
            header_name = header_element.text
        else:
            header_name = "Unknown Header"
        
        # Read the table into a DataFrame
        df = pd.read_html(str(table), header=0)[0]
        
        # Add a new column for header name
        df['Header'] = header_name
        
        dfs.append(df)
    return pd.concat(dfs)

def url_to_excel(df_in):
    lst = []
    for i, row in df_in.iterrows():
        url = str(row["url"])
        df = tables_wiki(url)

        lst.append(df)  
    return pd.concat(lst)

address_urls=input(" enter your url tables: ")
url_table = pd.read_excel(address_urls)

df_out=url_to_excel(url_table)
address_output=input("enter your output excel:  ")
df_out.to_excel(address_output)