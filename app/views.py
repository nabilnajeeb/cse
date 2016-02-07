from app import app
from flask import render_template

from bs4 import BeautifulSoup
import requests
import html5lib
from decimal import *

# In[316]:

def stock_info(table):
    price = float(tables.find_all('td')[3].get_text(strip=True).encode('utf-8'))
    prev_close = float(tables.find_all('td')[1].get_text(strip=True).encode('utf-8'))
    change_nosign = round(((price/prev_close-1)*100),2)
   
    if change_nosign >= 0: change = "+"+str(change_nosign) 
    else: change = str(change_nosign)
    
    stock_deets.extend([ticker,' ', price, ' ', change+'%','\n'])


# In[319]:

base_url = 'http://www.cse.lk/company_info.do?symbol='
stock_deets = []
tickers = ['TJL.N', 'ASIR.N', 'SHL.N', 'TKYO.N', 'TKYO.X', 'HHL.N', 'RCL.N', 'DIAL.N',]


# In[322]:

for ticker in tickers:
    print "souping", ticker
    url = base_url+str(ticker)+'0000'
    soup = BeautifulSoup(requests.get(url).text, 'html5lib')
    tables = soup.find_all('table', cellpadding="0", cellspacing="0", border="0", class_="ci_r")[0]
    stock_info(tables)


# In[323]:

text_out = ''.join(str(e) for e in stock_deets)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title = "Home", text = text_out, stock_deets = stock_deets)