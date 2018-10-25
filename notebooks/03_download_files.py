
# coding: utf-8

# In[1]:


import pandas as pd
import lxml.html as lh
import requests
import time
import os
import igc_validation


# In[92]:


def download_flight(flight_number):
    
    filename = "../docs/flights/flight_{}.igc".format(flight_number)
    print(filename)
    
    headers = {'User-Agent': 'Mozilla/5.0'}

    payload = {'type':'igc',
               'flightID': str(flight_number),
               'file': '',
               'captchaStr': '',
               'captcha': '',
              }

    session = requests.Session()
    res = session.post('http://xc.rmhpa.org/download_igc.php', headers=headers, data=payload)


    with open(filename, 'wb') as outfile:
        outfile.write(res.content)
     
    
    logbook = []
    logbook.append({'igcfile': os.path.abspath(filename)})
    try:
        for flight in logbook:
            flight = igc_validation.parse_igc(flight)

        for flight in logbook:
            flight = igc_validation.crunch_flight(flight)

        for flight in logbook:
            flight['outputfilename'] = igc_validation.get_output_filename(flight['igcfile'])
    except:
        filename = "flights_invalid/flight_{}.igc".format(flight_number)
        with open(filename, 'wb') as outfile:
            outfile.write(res.content)


# This will take about 3 hours... I have about 200 of them.

# In[93]:


df = pd.read_csv("clean/rmhpa_flights.csv")
records = df.to_dict(orient='records')
tic = time.time()

for i, rec in enumerate(records):
    url = rec['links']
    flight_number = url.split('/')[-1]
    
    if not os.path.exists("../docs/flights/flight_{}.igc".format(flight_number)): 
        print("---------------------------------------------")
        download_flight(flight_number)
        print(" #{} {} {}    {}% done....   {} seconds".format(flight_number, str(rec['index']), rec['distance'], round(i/len(records)*100), round(time.time()-tic)))
        time.sleep(1)

